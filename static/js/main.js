const provinceSelect = document.getElementById('province');
const citySelect = document.getElementById('city');



// ✅ 加载省份下拉选项
async function loadProvinces() {
  try {
    const response = await fetch('/provinces');
    const result = await response.json();
    const provinces = result.data?.provinces || [];

    provinces.forEach(province => {
      const option = document.createElement('option');
      option.value = province;
      option.textContent = province;
      provinceSelect.appendChild(option);
    });
  } catch (error) {
    console.error('❌ 加载省份失败:', error);
  }
}

// ✅ 加载城市列表（根据选中省份）
async function loadCities(province) {
  citySelect.innerHTML = '<option value="">请选择城市</option>';
  if (!province) return;

  try {
    const response = await fetch(`/cities?province=${encodeURIComponent(province)}`);
    const data = await response.json();
    const cities = data.data?.cities || [];

    cities.forEach(city => {
      const option = document.createElement('option');
      option.value = city;
      option.textContent = city;
      citySelect.appendChild(option);
    });
  } catch (error) {
    console.error('❌ 加载城市失败:', error);
  }
}

// ✅ 监听省份变化 → 加载城市
provinceSelect.addEventListener('change', function () {
  const selectedProvince = this.value;
  loadCities(selectedProvince);
});

// ✅ 获取或生成设备ID（存入 localStorage）
function getOrCreateDeviceId() {
  let deviceId = localStorage.getItem('device_id');
  if (!deviceId) {
    deviceId = crypto.randomUUID(); // 安全生成唯一 ID
    localStorage.setItem('device_id', deviceId);
  }
  return deviceId;
}

// ✅ 显示注册弹窗
function showRegisterModal() {
  const modal = document.getElementById('register-modal');
  modal.style.display = 'block';

  modal.querySelector('.close').onclick = () => modal.style.display = 'none';

  window.onclick = function (e) {
    if (e.target === modal) modal.style.display = 'none';
  };
}

// ✅ 预测表单提交
document.getElementById('predict-form').addEventListener('submit', async function (event) {
  event.preventDefault();
  const deviceId = getOrCreateDeviceId();

  const province = provinceSelect.value;
  const city = citySelect.value;
  const months = document.getElementById('months').value;
  const query_area = province + city;

  // 1️⃣ 请求 predict_click 日志记录
  try {
    const logResponse = await fetch('/predict_click', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        query_area: query_area,
        user_id: localStorage.getItem('user_id') || null,
        device_id: deviceId
      })
    });

    const logData = await logResponse.json();
    console.log('📌 点击记录结果:', logData);

    // ✅ 检查是否弹注册框
    if (logData.data?.show_register) {
      showRegisterModal();
    }
  } catch (err) {
    console.warn('❌ 日志记录失败:', err);
  }

  // 2️⃣ 发起预测请求
  try {
    const response = await fetch('/predict', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ province, city, months })
    });

    const data = await response.json();

    if (data && data.predicted_price !== undefined) {
      document.getElementById('price-output').textContent = `预计房价为：${data.predicted_price} 元`;
    } else {
      document.getElementById('price-output').textContent = '⚠️ 无法获取预测结果';
    }
  } catch (err) {
    console.error('❌ 预测接口调用失败:', err);
    document.getElementById('price-output').textContent = '❌ 预测失败，请稍后再试';
  }
});

let countdown = 60; // 倒计时秒数
let timer = null;

document.getElementById('send-code-btn').addEventListener('click', async function () {
  const phone = document.getElementById('reg-phone').value.trim();
  const btn = this;

  if (!phone) {
    alert('请输入手机号');
    return;
  }

  // 禁用按钮防止重复点击
  btn.disabled = true;
  btn.textContent = '发送中...';

  try {
    const res = await fetch('/send_sms_code', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ phone })
    });
    const result = await res.json();

    if (result.status === 'success') {
      alert('✅ 验证码已发送');
      startCountdown(btn);
    } else {
      alert(`❌ 发送失败：${result.message || '未知错误'}`);
      btn.disabled = false;
      btn.textContent = '重新发送';
    }
  } catch (err) {
    console.error(err);
    alert('❌ 网络异常，验证码发送失败');
    btn.disabled = false;
    btn.textContent = '重新发送';
  }
});

function startCountdown(btn) {
  countdown = 60;
  btn.disabled = true;
  btn.textContent = `${countdown}秒`;

  timer = setInterval(() => {
    countdown--;
    if (countdown <= 0) {
      clearInterval(timer);
      btn.disabled = false;
      btn.textContent = '重新发送';
    } else {
      btn.textContent = `${countdown}秒`;
    }
  }, 1000);
}

document.getElementById('open-register').addEventListener('click', function (e) {
  e.preventDefault(); // 阻止默认跳转
  showRegisterModal(); // 打开注册弹窗
});

// ✅ 注册表单提交
document.getElementById('register-form').addEventListener('submit', async function (e) {
  e.preventDefault();

  const username = document.getElementById('reg-username').value;
  const password = document.getElementById('reg-password').value;
  const phone = document.getElementById('reg-phone').value;
  const email = document.getElementById('reg-email').value;
const code = document.getElementById('reg-code').value;
  try {
    const response = await fetch('/register', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        username,
        password,
        phone,
        email,
        code  // 👈 提交验证码
      })
    });

    const result = await response.json();
   if (result.status === 'success') {
  alert('✅ 注册成功，请继续使用系统！');

  const now = new Date().getTime();
  localStorage.setItem('login_time', now);
  localStorage.setItem('user_id', result.user_id);
  localStorage.setItem('username', username ?? '');

  document.getElementById('register-modal').style.display = 'none';
  handleRegisterSuccess({
    username: username,
    avatar: '/static/images/default_avatar.png'
  });

    } else {
      alert(`❌ 注册失败：${result.message || '未知错误'}`);
    }
  } catch (err) {
    console.error('注册请求失败', err);
    alert('❌ 网络错误，注册失败');
  }
});
// 注册成功后右上角切换到用户
function handleRegisterSuccess(data) {
  const username = document.getElementById('reg-username').value;

  // 隐藏登录注册按钮
  document.getElementById('auth-buttons').style.display = 'none';

  // 显示用户信息区域
  const userInfo = document.getElementById('user-info');
  userInfo.style.display = 'flex';

  // 设置用户名和头像（你可以从服务器返回头像路径）
  document.getElementById('user-name').textContent = username;
  document.getElementById('user-avatar').src = '/static/images/default_avatar.png';
}
function showUserHeader() {
  const username = localStorage.getItem('username');
  const loginTime = localStorage.getItem('login_time');
  const now = new Date().getTime();

  // 7 天 = 7 * 24 * 60 * 60 * 1000 毫秒
  if (username && loginTime && now - loginTime < 7 * 24 * 60 * 60 * 1000) {
    document.querySelector('.top-buttons').innerHTML = `
      <div style="display: flex; align-items: center; gap: 8px;">
        <img src="/static/images/default_avatar.png" alt="头像" style="width: 32px; height: 32px; border-radius: 50%;">
        <span style="font-weight: bold; color: #333; font-size: 16px;">${username}</span>
      </div>
    `;
  } else {
    localStorage.clear(); // 超过 7 天自动清除信息
  }
}




window.addEventListener('DOMContentLoaded', () => {
  showUserHeader();
  loadProvinces();
  loadTrend();

  const username = localStorage.getItem('username');
  if (username) {
    document.getElementById('user-name').textContent = username;
    document.getElementById('user-info').style.display = 'flex';
    document.querySelector('.top-buttons').style.display = 'none';
  }
});

document.getElementById('logout-btn').addEventListener('click', () => {
  localStorage.removeItem('user_id');
  localStorage.removeItem('username');
  location.reload(); // 刷新页面
});
// 点击“登录”按钮，弹出登录框
document.getElementById('login-link').addEventListener('click', function (e) {
  e.preventDefault(); // 阻止跳转
  document.getElementById('login-modal').style.display = 'block';
});
// 点击关闭按钮 ×
document.getElementById('login-close').addEventListener('click', function () {
  document.getElementById('login-modal').style.display = 'none';
});

// 点击背景关闭弹窗
window.addEventListener('click', function (e) {
  if (e.target === document.getElementById('login-modal')) {
    document.getElementById('login-modal').style.display = 'none';
  }
});
// ✅ 登录表单提交逻辑
document.getElementById('login-form').addEventListener('submit', async function (e) {
  e.preventDefault();

  const username = document.getElementById('login-username').value.trim();
  const password = document.getElementById('login-password').value.trim();

  if (!username || !password) {
    alert('请输入用户名和密码');
    return;
  }

  try {
    const response = await fetch('/login', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ username, password })
    });

    const result = await response.json();

    if (result.status === 'success') {
      alert('✅ 登录成功');

      // 保存信息到 localStorage（保留 7 天）
      const now = new Date().getTime();
      localStorage.setItem('login_time', now);
      localStorage.setItem('username', result.data.username);
      localStorage.setItem('user_id', result.data.user_id);

      // 更新页面 UI
      document.getElementById('login-modal').style.display = 'none';
      document.getElementById('auth-buttons').style.display = 'none';
      document.getElementById('user-info').style.display = 'flex';
      document.getElementById('user-name').textContent = result.data.username;
    } else {
      alert(`❌ 登录失败：${result.message}`);
    }
  } catch (err) {
    console.error('❌ 登录请求失败:', err);
    alert('❌ 网络异常，无法登录');
  }
});
// ✅ 页面初始化
loadProvinces();
loadTrend();

// ✅ 加载趋势图
async function loadTrend() {
  try {
    const response = await fetch('/price_trend');
    const data = await response.json();
    document.getElementById('trend-chart').src = data.plot_url;
  } catch (error) {
    console.error('❌ 加载趋势图失败:', error);
  }
}
