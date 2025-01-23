from django.db import models


class ProtocolChoices(models.TextChoices):
    vmess = "vmess"
    vless = "vless"
    trojan = "trojan"
    shadow_socks = "shadow socks"
    tls = "tls"
    open_vpn = "open_vpn"
    wire_guard = "wire_guard"
    ikev2 = "ikev2"
    l2tp = "l2tp"
    sstp = "sstp"
    pptp = 'pptp'
    soft_ether = "soft_ether"
    open_connect = "open_connect"
