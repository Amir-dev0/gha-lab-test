document.addEventListener('DOMContentLoaded', () => {
  // ---------- 1. تغییر تم (دارک/روشن) ----------
  const themeToggle = document.getElementById('theme-toggle');
  const body = document.body;

  // بررسی تنظیمات ذخیره‌شده در مرورگر
  if (localStorage.getItem('theme') === 'dark') {
    body.classList.add('dark-mode');
    themeToggle.textContent = '☀️';
  }

  themeToggle.addEventListener('click', () => {
    body.classList.toggle('dark-mode');
    const isDark = body.classList.contains('dark-mode');
    themeToggle.textContent = isDark ? '☀️' : '🌙';
    localStorage.setItem('theme', isDark ? 'dark' : 'light');
  });

  // ---------- 2. دکمه «شروع کنید» با پیام‌های متغیر ----------
  const startBtn = document.querySelector('.btn');
  let clickCount = 0;

  const messageList = [
    '🎉 خوش آمدید!',
    '👋 سلام دوباره!',
    '❤️ ممنون از کلیک شما!',
    '✨ صفحه‌ات زیباتر شد!',
    '🚀 به دنیای طراحی خوش آمدید!',
    '💫 چه انتخاب خوبی!',
    '🌟 درخشش با توست!'
  ];

  startBtn.addEventListener('click', (e) => {
    e.preventDefault(); // جلوگیری از تغییر صفحه (چون لینک است)
    clickCount++;
    const message = messageList[clickCount % messageList.length];
    showToast(message);
  });

  // ---------- 3. تابع نمایش پیام (Toast) ----------
  function showToast(message) {
    // اگر پیام قبلی هنوز وجود دارد، حذفش می‌کنیم
    const existingToast = document.querySelector('.toast');
    if (existingToast) {
      existingToast.remove();
    }

    // ساخت المان جدید
    const toast = document.createElement('div');
    toast.className = 'toast';
    toast.textContent = message;
    document.body.appendChild(toast);

    // حذف خودکار بعد از ۳ ثانیه
    setTimeout(() => {
      toast.classList.add('hide');
      setTimeout(() => {
        toast.remove();
      }, 400);
    }, 3000);
  }

  // ---------- 4. یک پیام در کنسول برای تایید اجرا ----------
  console.log('✨ صفحه با جاوااسکریپت فعال شد!');
});
