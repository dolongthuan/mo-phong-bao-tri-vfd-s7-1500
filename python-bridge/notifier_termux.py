"""Kich hoat rung + thong bao goc Android + doc to canh bao (TTS) tren dien
thoai qua Termux:API, ket noi SSH toi Termux dang chay tren dien thoai (khong
qua Telegram/Twilio).

Yeu cau tren dien thoai:
- App Termux + goi `openssh` (`pkg install openssh`), da chay `sshd` (port mac
  dinh 8022)
- App Termux:API (cai tu F-Droid/Google Play, cung id voi Termux dang dung) +
  goi `termux-api` (`pkg install termux-api`)

Neu khong dien du TERMUX_HOST/TERMUX_USER/TERMUX_PASSWORD trong .env, ham
notify() se bo qua (khong lam crash chuong trinh chinh).
"""
from __future__ import annotations

import json
import logging

logger = logging.getLogger(__name__)

# termux-tts-speak (va cac lenh Termux:API khac) doi khi khong bao gio tra ve
# exit status (vd service TTS bi ket, gap khi goi lien tiep 2 lan) - gioi han
# thoi gian cho de KHONG bao gio lam treo vong lap poll chinh cua main_bridge.py.
# TTS doc het 1 canh bao day du co the mat 20-30s, nen can rieng 1 nguong dai hon.
_QUICK_COMMAND_TIMEOUT_SEC = 10
_SPEAK_TIMEOUT_SEC = 60


def _shell_quote(text: str) -> str:
    return "'" + text.replace("'", "'\\''") + "'"


def _exec(client, cmd: str, timeout: float = _QUICK_COMMAND_TIMEOUT_SEC):
    """Chay 1 lenh qua SSH, cho toi da `timeout` giay. Tra ve (True, stdout_text)
    neu thanh cong, (False, "") neu that bai/qua thoi gian cho."""
    _, stdout, stderr = client.exec_command(cmd)
    if not stdout.channel.status_event.wait(timeout):
        stdout.channel.close()
        logger.warning("Lenh Termux qua thoi gian cho (%ss), bo qua: %s", timeout, cmd)
        return False, ""
    exit_status = stdout.channel.recv_exit_status()
    if exit_status != 0:
        logger.warning("Lenh Termux that bai (%s): %s", cmd, stderr.read().decode(errors="ignore"))
        return False, ""
    return True, stdout.read().decode(errors="ignore")


def _max_out_volume(client, stream: str) -> None:
    """Day am luong cua 1 stream (vd 'alarm') len max - stream ALARM co muc am
    luong rieng, khong bi nut volume vat ly (thuong chi chinh media/chuong) anh
    huong, nen TTS phat qua stream nay co the rat nho du da "mo full am thanh".
    """
    ok, output = _exec(client, "termux-volume")
    if not ok:
        return
    try:
        streams = json.loads(output)
        max_volume = next(s["max_volume"] for s in streams if s["stream"] == stream)
    except (json.JSONDecodeError, StopIteration, KeyError):
        logger.warning("Khong doc duoc muc am luong toi da cua stream '%s'", stream)
        return
    _exec(client, f"termux-volume {stream} {max_volume}")


def notify(
    host: str,
    port: int,
    username: str,
    password: str,
    title: str,
    content: str,
    vibrate_ms: int = 1000,
) -> bool | None:
    if not all([host, username, password]):
        logger.info("Chua cau hinh TERMUX_* - bo qua rung/thong bao dien thoai.")
        return None

    try:
        import paramiko
    except ImportError:
        logger.warning("Chua cai paramiko (pip install paramiko) - bo qua rung/thong bao dien thoai.")
        return None

    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(host, port=port, username=username, password=password, timeout=10)
    except Exception:
        logger.exception("Ket noi SSH toi Termux that bai")
        return False

    try:
        vibrate_cmd = f"termux-vibrate -d {vibrate_ms} -f"
        notify_cmd = (
            "termux-notification "
            f"--title {_shell_quote(title)} "
            f"--content {_shell_quote(content)} "
            "--priority high "
            f"--vibrate {vibrate_ms}"
        )
        speak_cmd = f"termux-tts-speak -l vi -s ALARM {_shell_quote(content)}"

        _max_out_volume(client, "alarm")

        all_ok = True
        for cmd in (vibrate_cmd, notify_cmd):
            ok, _ = _exec(client, cmd)
            all_ok = all_ok and ok

        ok, _ = _exec(client, speak_cmd, timeout=_SPEAK_TIMEOUT_SEC)
        all_ok = all_ok and ok

        return all_ok
    except Exception:
        logger.exception("Loi khi chay lenh Termux qua SSH")
        return False
    finally:
        client.close()
