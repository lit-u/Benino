
import asyncio
import json
import websockets
import qrcode
import os
import sys

async def get_qr():
    uri = "ws://localhost:3001"
    print(f"Connecting to {uri}...")
    try:
        async with websockets.connect(uri) as websocket:
            print("Connected! Waiting for QR code...")
            while True:
                message = await websocket.recv()
                data = json.loads(message)
                
                if data.get("type") == "qr":
                    qr_data = data.get("qr")
                    print("QR code received!")
                    
                    # Generate image
                    img = qrcode.make(qr_data)
                    img_path = os.path.abspath("whatsapp_qr.png")
                    img.save(img_path)
                    
                    print(f"QR code saved to: {img_path}")
                    
                    # Open the image
                    if sys.platform == "win32":
                        os.startfile(img_path)
                    else:
                        import subprocess
                        subprocess.call(["open", img_path])
                        
                    print("Image opened. Please scan it with WhatsApp.")
                    break
                
                elif data.get("type") == "status":
                    print(f"Status: {data.get('status')}")
                    if data.get("status") == "connected":
                        print("Already connected!")
                        break

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(get_qr())
