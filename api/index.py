import json
import blackboxprotobuf
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from fastapi import FastAPI, Form, Request, Response
from fastapi.responses import HTMLResponse, JSONResponse
import httpx
from mangum import Mangum

app = FastAPI()
handler = Mangum(app)

MAIN_KEY = b"Yg&tc%DEuh6%Zc^8"
MAIN_IV = b"6oyZDr22E3ychjM%"
BASE_TARGET_URL = "https://loginbp.ggpolarbear.com"

ACTIVE_CONFIG = {
    "open_id": None,
    "access_token": None
}

VER_DATA = {
    "code": 0,
    "is_server_open": True,
    "is_firewall_open": False,
    "cdn_url": "https://dl.cdn.freefiremobile.com/live/ABHotUpdates/",
    "backup_cdn_url": "https://dl.cdn.freefiremobile.com/live/ABHotUpdates/",
    "abhotupdate_cdn_url": "https://dl-core.cdn.freefiremobile.com/live/ABHotUpdates/",
    "img_cdn_url": "https://dl.cdn.freefiremobile.com/common/",
    "login_download_optionalpack": "optionalclothres:shaders|optionalpetres:optionalpetres_commonab_shader|optionallobbyres:",
    "need_track_hotupdate": True,
    "abhotupdate_check": "cache_res;assetindexer;SH-Gpp",
    "latest_release_version": "OB54",
    "min_hint_size": 1,
    "space_required_in_GB": 1.48,
    "should_check_ab_load": False,
    "force_refresh_restype": "optionalavatarres",
    "remote_version": "1.130.22",
    "server_url": "https://bahlil.embege-enak-loh.my.id/",
    "is_review_server": False,
    "use_login_optional_download": True,
    "use_background_download": False,
    "use_background_download_lobby": False,
    "country_code": "SG",
    "client_ip": "23.236.119.226",
    "gdpr_version": 0,
    "billboard_cdn_url": "https://dl.dir.freefiremobile.com/common/OB54/CSH/patchupdate/sgolzjifnmi101.ff_extend;https://dl.dir.freefiremobile.com/common/OB54/CSH/patchupdate/sgolzjifnmi102.ff_extend;https://dl.dir.freefiremobile.com/common/OB54/CSH/patchupdate/sgolzjifnmi103.ff_extend;https://dl.dir.freefiremobile.com/common/OB54/CSH/patchupdate/sgolzjifnmi104.ff_extend;https://dl.dir.freefiremobile.com/common/OB54/CSH/patchupdate/sgolzjifnmi105.ff_extend;https://dl.dir.freefiremobile.com/common/OB54/CSH/patchupdate/sgolzjifnmi106.ff_extend;https://dl.dir.freefiremobile.com/common/OB54/CSH/patchupdate/sgolzjifnmi107.ff_extend",
    "billboard_msg": "",
    "web_url": "",
    "billboard_bg_url": "https://dl.cdn.freefiremobile.com/common/OB23/version/Patch_Bg.png",
    "max_store": "",
    "max_web": "",
    "max_video": "",
    "patchnote_url": "https://dl.dir.freefiremobile.com/common/web_event/aswqooiwd/zClWsKYO.html?lang=en",
    "multi_region": "",
    "need_check_ip_list": [],
    "network_log_server": "https://sgnetwork.ggblueshark.com/",
    "web_log_server": "https://networkselftest.ff.garena.com/api/",
    "login_failed_count": 2,
    "test_url": "",
    "core_url": "csoversea.castle.freefiremobile.com",
    "core_ip_list": ["0.0.0.0", "50.109.27.134", "129.226.2.163", "129.226.1.13", "129.226.1.16"],
    "appstore_url": "http://play.google.com/store/apps/details?id=com.dts.freefireth",
    "backup_appstore_url": "",
    "garena_login": False,
    "garena_hint": False,
    "gop_url": "",
    "gamevar": "var_name,comment,var_type,var_value,var_region,var_platform\nvar_name,comment,var_type,var_value,var_region,var_platform\nEnableVariableFFVoiceIDC,EnableVariableFFVoiceIDC,bool,False,,\nEnableYieldMutexDuringAsyncLoad,EnableYieldMutexDuringAsyncLoad,bool,False,,\nNinthProgressLoadingDuration,NinthProgressLoadingDuration,float,0,,\nEnableUGCScrollViewCulling,EnableUGCScrollViewCulling,bool,False,,\nEnableUGCScrollViewCulling,EnableUGCScrollViewCulling,bool,False,,\nReservedInt01,ReservedInt01,int,5,,\nNinthLevelPortalRadius,NinthLevelPortalRadius,float,20,,\nEnable2018ABstreamed,Enable2018ABstreamed,bool,False,,ios\nEnableAsyncCullResultsRelease,EnableAsyncCullResultsRelease,bool,False,,ios\nReservedInt02,ReservedInt02,int,30,,\nEnableUGCHalfwayJoin,EnableUGCHalfwayJoin,bool,False,,\nLadderMatchSplashRegionOn,LadderMatchSplashRegionOn,string,PK;EUROPE;TH;SG;TW;BR,,\nSensitivityMaxSetting,SensitivityMaxSetting,float,8.5,,\nSensitivity1PMaxSetting,Sensitivity1PMaxSetting,float,8.5,,\nX1ScopeMaxSetting,X1ScopeMaxSetting,float,8.5,,\nX2ScopeMaxSetting,X2ScopeMaxSetting,float,8.5,,\nX4ScopeMaxSetting,X4ScopeMaxSetting,float,8.5,,\nX8ScopeMaxSetting,X8ScopeMaxSetting,float,8.5,,\nFreeLookMaxSetting,FreeLookMaxSetting,float,8.5,,\nPlayerOutlineWidthSpecial,PlayerOutlineWidthSpecial,float,8.5,,\n",
    "remote_option_version": "optionallocres:50|optionalavatarres:791|optionalclothres:1228|optionalfootballres:27|optionalfullscreencgres:319|optionalhuntinggroundres:246|optionalinfection:125|optionalingameres:503|optionallobbyres:640|optionallonewolfres:86|optionallonewolfstrikeoutres:59|optionalludores:42|optionalmap1res:385|optionalmap2res:156|optionalmap4res:139|optionalmaphippores:118|optionalmapres:357|optionalnewblast:163|optionalpetres:910|optionalrushb:108|optionalrushingpetsres:84|optionalsnowduelres:65|optionalsocialres:223|optionaltrainingres:297|optionalugcres:844|optionalvoiceres:344|optionalwerewolves:153|optionalwerunres:92|optionalmapponyres:204|optionalugcoldparadiseres:34|optionalmultiregionres:29",
    "remote_option_version_astc": "optionallocres:50|optionalavatarres:753|optionalclothres:1228|optionalfootballres:29|optionalfullscreencgres:306|optionalhuntinggroundres:216|optionalinfection:124|optionalingameres:461|optionallobbyres:640|optionallonewolfres:206|optionallonewolfstrikeoutres:155|optionalludores:175|optionalmap1res:385|optionalmap2res:192|optionalmap4res:175|optionalmaphippores:120|optionalmapres:391|optionalnewblast:162|optionalpetres:910|optionalrushb:241|optionalrushingpetsres:217|optionalsnowduelres:65|optionalsocialres:215|optionaltrainingres:267|optionalugcres:786|optionalvoiceres:379|optionalwerewolves:286|optionalwerunres:81|optionalmapponyres:204|optionalugcoldparadiseres:33|optionalmultiregionres:27",
    "ggp_url": "gin.freefiremobile.com",
}


def aes_decrypt(data: bytes) -> bytes:
    cipher = AES.new(MAIN_KEY, AES.MODE_CBC, MAIN_IV)
    decrypted = cipher.decrypt(data)
    return unpad(decrypted, AES.block_size)


def aes_encrypt(data: bytes) -> bytes:
    cipher = AES.new(MAIN_KEY, AES.MODE_CBC, MAIN_IV)
    return cipher.encrypt(pad(data, AES.block_size))


def make_octet_response(text: str, status_code: int = 400) -> Response:
    return Response(
        content=text.encode("utf-8"),
        status_code=status_code,
        media_type="application/octet-stream",
    )


@app.get("/dashboard", response_class=HTMLResponse)
@app.get("/DASHBOARD", response_class=HTMLResponse)
async def dashboard_view():
    current_oid = ACTIVE_CONFIG.get("open_id") or "None"
    current_tok = ACTIVE_CONFIG.get("access_token") or "None"
    is_active = bool(ACTIVE_CONFIG.get("open_id") and ACTIVE_CONFIG.get("access_token"))

    html_content = f"""<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>MajorLogin Control Center</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet">
    <style>
        * {{
            box-sizing: border-box;
            margin: 0;
            padding: 0;
            font-family: "Plus Jakarta Sans", -apple-system, BlinkMacSystemFont, sans-serif;
        }}
        body {{
            background: radial-gradient(circle at 50% 0%, #172554 0%, #030712 70%);
            color: #f8fafc;
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 24px;
        }}
        .container {{
            width: 100%;
            max-width: 540px;
            background: rgba(15, 23, 42, 0.75);
            backdrop-filter: blur(20px);
            -webkit-backdrop-filter: blur(20px);
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 24px;
            padding: 32px;
            box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.7), 0 0 40px rgba(56, 189, 248, 0.1);
        }}
        .header {{
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin-bottom: 24px;
        }}
        .header-title h1 {{
            font-size: 1.35rem;
            font-weight: 800;
            letter-spacing: -0.02em;
            color: #fff;
            display: flex;
            align-items: center;
            gap: 8px;
        }}
        .header-title h1 span {{
            background: linear-gradient(135deg, #38bdf8, #818cf8);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }}
        .header-title p {{
            font-size: 0.82rem;
            color: #94a3b8;
            margin-top: 2px;
        }}
        .badge {{
            display: inline-flex;
            align-items: center;
            gap: 6px;
            font-size: 0.72rem;
            font-weight: 700;
            padding: 4px 10px;
            border-radius: 9999px;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }}
        .badge-active {{
            background: rgba(34, 197, 94, 0.12);
            color: #4ade80;
            border: 1px solid rgba(34, 197, 94, 0.3);
        }}
        .badge-inactive {{
            background: rgba(239, 68, 68, 0.12);
            color: #f87171;
            border: 1px solid rgba(239, 68, 68, 0.3);
        }}
        .dot {{
            width: 6px;
            height: 6px;
            border-radius: 50%;
            background: currentColor;
            box-shadow: 0 0 8px currentColor;
        }}
        .status-card {{
            background: rgba(2, 6, 23, 0.6);
            border: 1px solid rgba(255, 255, 255, 0.06);
            border-radius: 16px;
            padding: 16px;
            margin-bottom: 24px;
        }}
        .status-row {{
            display: flex;
            flex-direction: column;
            gap: 4px;
            margin-bottom: 12px;
        }}
        .status-row:last-child {{
            margin-bottom: 0;
        }}
        .status-label {{
            font-size: 0.72rem;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            color: #64748b;
            font-weight: 700;
        }}
        .status-val {{
            font-family: "JetBrains Mono", monospace;
            font-size: 0.85rem;
            color: #38bdf8;
            word-break: break-all;
            background: rgba(15, 23, 42, 0.5);
            padding: 6px 10px;
            border-radius: 8px;
            border: 1px solid rgba(255, 255, 255, 0.03);
        }}
        .form-group {{
            margin-bottom: 18px;
        }}
        label {{
            display: block;
            font-size: 0.8rem;
            font-weight: 600;
            color: #cbd5e1;
            margin-bottom: 8px;
        }}
        input[type="text"] {{
            width: 100%;
            padding: 12px 16px;
            background: rgba(2, 6, 23, 0.8);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 12px;
            color: #fff;
            font-size: 0.9rem;
            font-family: "JetBrains Mono", monospace;
            outline: none;
            transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
        }}
        input[type="text"]:focus {{
            border-color: #38bdf8;
            box-shadow: 0 0 0 3px rgba(56, 189, 248, 0.15);
            background: rgba(2, 6, 23, 0.95);
        }}
        .btn-group {{
            display: flex;
            gap: 10px;
            margin-top: 10px;
        }}
        button {{
            flex: 1;
            padding: 13px;
            border-radius: 12px;
            font-size: 0.9rem;
            font-weight: 700;
            cursor: pointer;
            transition: all 0.2s ease;
            border: none;
        }}
        .btn-primary {{
            background: linear-gradient(135deg, #0284c7, #2563eb);
            color: #fff;
            box-shadow: 0 4px 14px rgba(37, 99, 235, 0.3);
        }}
        .btn-primary:hover {{
            background: linear-gradient(135deg, #0369a1, #1d4ed8);
            transform: translateY(-1px);
        }}
        .btn-secondary {{
            background: rgba(255, 255, 255, 0.05);
            color: #94a3b8;
            border: 1px solid rgba(255, 255, 255, 0.08);
            flex: 0 0 100px;
        }}
        .btn-secondary:hover {{
            background: rgba(255, 255, 255, 0.08);
            color: #f8fafc;
        }}
        .notification {{
            margin-top: 18px;
            padding: 12px 16px;
            border-radius: 12px;
            background: rgba(34, 197, 94, 0.1);
            border: 1px solid rgba(34, 197, 94, 0.2);
            color: #4ade80;
            font-size: 0.82rem;
            font-weight: 500;
            display: none;
            align-items: center;
            gap: 8px;
            animation: fadeIn 0.3s ease;
        }}
        @keyframes fadeIn {{
            from {{ opacity: 0; transform: translateY(4px); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <div class="header-title">
                <h1><span>MajorLogin</span> Control</h1>
                <p>Interceptor & Payload Override Center</p>
            </div>
            <div id="statusBadge" class="badge {'badge-active' if is_active else 'badge-inactive'}">
                <span class="dot"></span>
                <span id="badgeText">{'Active' if is_active else 'Standby'}</span>
            </div>
        </div>

        <div class="status-card">
            <div class="status-row">
                <span class="status-label">Active OpenID (Field 22)</span>
                <div class="status-val" id="statOid">{current_oid}</div>
            </div>
            <div class="status-row">
                <span class="status-label">Active Access Token (Field 29)</span>
                <div class="status-val" id="statTok">{current_tok}</div>
            </div>
        </div>

        <form id="cfgForm">
            <div class="form-group">
                <label for="open_id">Open ID (Field 22)</label>
                <input type="text" id="open_id" name="open_id" placeholder="Contoh: 1234567890" autocomplete="off" required>
            </div>
            
            <div class="form-group">
                <label for="access_token">Access Token (Field 29)</label>
                <input type="text" id="access_token" name="access_token" placeholder="Tempel token target di sini" autocomplete="off" required>
            </div>

            <div class="btn-group">
                <button type="button" class="btn-secondary" id="resetBtn">Reset</button>
                <button type="submit" class="btn-primary" id="submitBtn">Apply Override</button>
            </div>
        </form>

        <div class="notification" id="notifBox">
            <svg width="16" height="16" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path></svg>
            <span id="notifText">Configuration updated successfully!</span>
        </div>
    </div>

    <script>
        const form = document.getElementById('cfgForm');
        const submitBtn = document.getElementById('submitBtn');
        const resetBtn = document.getElementById('resetBtn');
        const notifBox = document.getElementById('notifBox');
        const notifText = document.getElementById('notifText');
        const badge = document.getElementById('statusBadge');
        const badgeText = document.getElementById('badgeText');
        const statOid = document.getElementById('statOid');
        const statTok = document.getElementById('statTok');

        function showNotification(msg) {{
            notifText.innerText = msg;
            notifBox.style.display = 'flex';
            setTimeout(() => {{
                notifBox.style.display = 'none';
            }}, 4000);
        }}

        form.addEventListener('submit', async (e) => {{
            e.preventDefault();
            submitBtn.disabled = true;
            submitBtn.innerText = "Applying...";

            const oid = document.getElementById('open_id').value.trim();
            const tok = document.getElementById('access_token').value.trim();

            const formData = new FormData();
            formData.append('open_id', oid);
            formData.append('access_token', tok);

            try {{
                const res = await fetch('/api/set-config', {{
                    method: 'POST',
                    body: formData
                }});
                const data = await res.json();
                if(data.status === 'success') {{
                    statOid.innerText = oid;
                    statTok.innerText = tok;
                    badge.className = 'badge badge-active';
                    badgeText.innerText = 'Active';
                    showNotification('Override berhasil aktif untuk /MajorLogin!');
                    form.reset();
                }}
            }} catch (err) {{
                showNotification('Gagal mengupdate konfigurasi!');
            }} finally {{
                submitBtn.disabled = false;
                submitBtn.innerText = "Apply Override";
            }}
        }});

        resetBtn.addEventListener('click', async () => {{
            const formData = new FormData();
            formData.append('open_id', '');
            formData.append('access_token', '');
            
            try {{
                await fetch('/api/set-config', {{
                    method: 'POST',
                    body: formData
                }});
                statOid.innerText = 'None';
                statTok.innerText = 'None';
                badge.className = 'badge badge-inactive';
                badgeText.innerText = 'Standby';
                showNotification('Konfigurasi berhasil direset (Forward Normal).');
                form.reset();
            }} catch (err) {{
                showNotification('Gagal mereset konfigurasi!');
            }}
        }});
    </script>
</body>
</html>
"""
    return HTMLResponse(content=html_content)


@app.post("/api/set-config")
async def set_config(open_id: str = Form(""), access_token: str = Form("")):
    ACTIVE_CONFIG["open_id"] = open_id.strip() if open_id.strip() else None
    ACTIVE_CONFIG["access_token"] = access_token.strip() if access_token.strip() else None
    return {"status": "success", "open_id": ACTIVE_CONFIG["open_id"]}


@app.post("/MajorLogin")
@app.post("/majorlogin")
@app.post("/api/MajorLogin")
@app.post("/api/majorlogin")
async def handle_major_login(request: Request):
    body = await request.body()
    if not body:
        return make_octet_response("Request body is empty\n", status_code=400)

    modified_body = body
    is_hex_input = False

    try:
        try:
            ciphertext = bytes.fromhex(body.decode("utf-8", errors="ignore").strip())
            is_hex_input = True
        except Exception:
            ciphertext = body

        if len(ciphertext) > 0 and len(ciphertext) % 16 == 0:
            decrypted = aes_decrypt(ciphertext)
            
            # Decode message langsung agar tipe native (int/bytes/str) tidak korup menjadi string
            decoded_dict, typedef = blackboxprotobuf.decode_message(decrypted)

            if ACTIVE_CONFIG.get("open_id") and ACTIVE_CONFIG.get("access_token"):
                raw_oid = ACTIVE_CONFIG["open_id"]
                if "22" in typedef and typedef["22"].get("type") in ["int", "uint", "varint"]:
                    decoded_dict["22"] = int(raw_oid)
                else:
                    decoded_dict["22"] = str(raw_oid)

                raw_tok = ACTIVE_CONFIG["access_token"]
                if "29" in typedef and typedef["29"].get("type") == "bytes":
                    decoded_dict["29"] = raw_tok.encode("utf-8")
                else:
                    decoded_dict["29"] = str(raw_tok)

            re_encoded_proto = blackboxprotobuf.encode_message(decoded_dict, typedef)
            re_encrypted = aes_encrypt(re_encoded_proto)

            modified_body = (
                re_encrypted.hex().encode("utf-8") if is_hex_input else re_encrypted
            )

    except Exception as e:
        print(f"[Warn] Failed to override payload: {e}")
        modified_body = body

    headers = dict(request.headers)
    headers.pop("host", None)
    headers.pop("content-length", None)

    async with httpx.AsyncClient(timeout=30.0) as client:
        try:
            target_res = await client.post(
                f"{BASE_TARGET_URL}/MajorLogin",
                content=modified_body,
                headers=headers,
            )
            return Response(
                content=target_res.content,
                status_code=target_res.status_code,
                headers=dict(target_res.headers),
            )
        except Exception as e:
            return make_octet_response(
                f"Proxy Error: [FFFFFF]{str(e)}\n", status_code=502
            )


@app.api_route(
    "/{path:path}",
    methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS", "HEAD"],
)
async def catch_all(request: Request, path: str):
    if "ver.php" in path.lower():
        return JSONResponse(content=VER_DATA, status_code=200)

    target_url = f"{BASE_TARGET_URL}/{path}"
    if request.url.query:
        target_url += f"?{request.url.query}"

    headers = dict(request.headers)
    headers.pop("host", None)
    headers.pop("content-length", None)

    body = await request.body()
    async with httpx.AsyncClient(timeout=30.0) as client:
        try:
            target_res = await client.request(
                method=request.method,
                url=target_url,
                headers=headers,
                content=body if body else None,
            )
            return Response(
                content=target_res.content,
                status_code=target_res.status_code,
                headers=dict(target_res.headers),
            )
        except Exception as e:
            return make_octet_response(
                f"Proxy Error: [FFFFFF]{str(e)}\n", status_code=502
            )
