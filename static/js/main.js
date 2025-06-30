 const provinceSelect = document.getElementById('province');
  const citySelect = document.getElementById('city');

// 👉 用户选择省份时，动态加载城市
provinceSelect.addEventListener('change', function () {
  const selectedProvince = this.value;
  loadCities(selectedProvince); // 调用你之前写的函数
});

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
console.log(cities);
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

  // ✅ 提交预测表单
  document.getElementById('predict-form').addEventListener('submit', async function (event) {
    event.preventDefault();

    const province = provinceSelect.value;
    const city = citySelect.value;
    const months = document.getElementById('months').value;
    const query_area = province + city;

    try {
      // 记录点击日志
      const logResponse = await fetch('/predict_click', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          query_area: query_area,
          user_id: localStorage.getItem('user_id') || null
        })
      });

      const logData = await logResponse.json();
      console.log('📌 点击记录结果:', logData);

      if (logData.show_register) {
        alert('🔔 您多次使用该功能，建议注册获取完整功能体验。');
      }
    } catch (err) {
      console.warn('❌ 日志记录失败:', err);
    }

    try {
      // 获取预测结果
      const response = await fetch('/predict', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ province, city, months })
      });

      const data = await response.json();
      document.getElementById('price-output').textContent = `预计房价为：${data.predicted_price} 元`;
    } catch (err) {
      console.error('❌ 预测接口调用失败:', err);
    }
  });

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

  // 页面初始化调用
  loadProvinces();
  loadTrend();