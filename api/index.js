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
    current_oid = ACTIVE_CONFIG.get("open_id") or "Belum diatur"
    current_tok = (
        (ACTIVE_CONFIG["access_token"][:15] + "...")
        if ACTIVE_CONFIG.get("access_token")
        else "Belum diatur"
    )

    html_content = f"""<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>MajorLogin Control Dashboard</title>
    <style>
        * {{ box-sizing: border-box; margin: 0; padding: 0; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; }}
        body {{ background: #0b0f19; color: #f1f5f9; display: flex; justify-content: center; align-items: center; min-height: 100vh; padding: 20px; }}
        .card {{ background: #111827; width: 100%; max-width: 520px; padding: 32px; border-radius: 16px; border: 1px solid #1f2937; box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5); }}
        h1 {{ font-size: 1.4rem; font-weight: 700; color: #38bdf8; margin-bottom: 6px; }}
        p.subtitle {{ font-size: 0.85rem; color: #9ca3af; margin-bottom: 20px; }}
        .status-box {{ background: #030712; padding: 12px 16px; border-radius: 8px; border: 1px solid #374151; margin-bottom: 20px; font-size: 0.85rem; }}
        .status-item {{ display: flex; justify-content: space-between; margin-bottom: 4px; }}
        .status-item:last-child {{ margin-bottom: 0; }}
        .status-label {{ color: #94a3b8; }}
        .status-val {{ color: #4ade80; font-family: monospace; }}
        .form-group {{ margin-bottom: 16px; }}
        label {{ display: block; font-size: 0.8rem; font-weight: 600; margin-bottom: 6px; color: #e2e8f0; letter-spacing: 0.025em; }}
        input[type="text"] {{ width: 100%; padding: 12px 14px; background: #1f2937; border: 1px solid #374151; border-radius: 8px; color: #fff; font-size: 0.95rem; outline: none; transition: 0.2s; }}
        input[type="text"]:focus {{ border-color: #38bdf8; }}
        button {{ width: 100%; padding: 12px; background: #0284c7; color: white; border: none; border-radius: 8px; font-size: 0.95rem; font-weight: 600; cursor: pointer; transition: 0.2s; margin-top: 8px; }}
        button:hover {{ background: #0369a1; }}
        .result-box {{ margin-top: 20px; padding: 14px; background: #030712; border-radius: 8px; border: 1px dashed #38bdf8; display: none; }}
        .result-title {{ font-size: 0.75rem; text-transform: uppercase; color: #38bdf8; font-weight: 700; margin-bottom: 4px; }}
        .msg-box {{ font-size: 0.9rem; color: #4ade80; }}
    </style>
</head>
<body>
    <div class="card">
        <h1>MajorLogin Override Control</h1>
        <p class="subtitle">Atur OpenID dan Access Token yang otomatis diterapkan ke /MajorLogin.</p>
        
        <div class="status-box">
            <div class="status-item">
                <span class="status-label">Active OpenID:</span>
                <span class="status-val" id="statOid">{current_oid}</span>
            </div>
            <div class="status-item">
                <span class="status-label">Active Token:</span>
                <span class="status-val" id="statTok">{current_tok}</span>
            </div>
        </div>

        <form id="cfgForm">
            <div class="form-group">
                <label for="open_id">OPEN ID (Field 22)</label>
                <input type="text" id="open_id" name="open_id" placeholder="Masukkan OpenID target" required>
            </div>
            
            <div class="form-group">
                <label for="access_token">ACCESS TOKEN (Field 29)</label>
                <input type="text" id="access_token" name="access_token" placeholder="Masukkan Access Token" required>
            </div>

            <button type="submit" id="submitBtn">Save Configuration</button>
        </form>

        <div class="result-box" id="resultBox">
            <div class="result-title">Status</div>
            <div class="msg-box" id="resultMsg"></div>
        </div>
    </div>

    <script>
        document.getElementById('cfgForm').addEventListener('submit', async (e) => {{
            e.preventDefault();
            const btn = document.getElementById('submitBtn');
            btn.disabled = true;
            btn.innerText = "Saving...";

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
                    document.getElementById('statOid').innerText = oid;
                    document.getElementById('statTok').innerText = tok.length > 15 ? tok.substring(0, 15) + "..." : tok;
                    document.getElementById('resultMsg').innerText = "Konfigurasi aktif berhasil diupdate! Request /MajorLogin sekarang otomatis memakai akun ini.";
                    document.getElementById('resultBox').style.display = 'block';
                }}
            }} catch (err) {{
                console.error(err);
            }} finally {{
                btn.disabled = false;
                btn.innerText = "Save Configuration";
            }}
        }});
    </script>
</body>
</html>
"""
    return HTMLResponse(content=html_content)


@app.post("/api/set-config")
async def set_config(open_id: str = Form(...), access_token: str = Form(...)):
    ACTIVE_CONFIG["open_id"] = open_id.strip()
    ACTIVE_CONFIG["access_token"] = access_token.strip()
    return {"status": "success", "open_id": open_id}


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
            decoded_dict, typedef = blackboxprotobuf.protobuf_to_json(decrypted)

            if isinstance(decoded_dict, str):
                decoded_dict = json.loads(decoded_dict)

            if ACTIVE_CONFIG.get("open_id") and ACTIVE_CONFIG.get("access_token"):
                decoded_dict["22"] = str(ACTIVE_CONFIG["open_id"])
                decoded_dict["29"] = str(ACTIVE_CONFIG["access_token"])

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
