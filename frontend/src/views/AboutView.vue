<template>
  <div class="wraper">
    <h1>關於這個部落格</h1>
    <div class="content">
      <section>
        <h2>簡介</h2>
        <p>
          這是一個訂閱制部落格平台的專案，使用者可以註冊帳號並訂閱文章內容。
          除了傳統信用卡支付，平台也支援加密貨幣付款，提供更多元的支付方式。
          目前這是 MVP 版本，未來會持續開發更多功能與改進體驗。
        </p>
      </section>

      <section class="mb-8">
        <h2>開發動機</h2>
        <p>
          我希望建立一個平台，記錄日常生活與工作中學習到的技術與心得。
          隨著訂閱經濟的興起，內容訂閱服務越來越流行。我也希望能開發一個屬於自己的訂閱服務，而不依賴第三方，可以完全掌控平台、內容與訂閱用戶。
        </p>
        <p>
          另外，作為後端工程師，我也想藉由此機會實作一個完整的全端專案，目前使用 Vue 前端框架，後端使用 Django REST API，實現前後端分離。
        </p>
      </section>

      <section>
        <h2>核心功能</h2>
        <ul>
          <li>發佈文章、文章分類、標籤管理</li>
          <li>使用者留言與回覆功能</li>
          <li>Google OAuth 登入</li>
          <li>用戶訂閱（Paddle 信用卡支付 / NowPayments 加密貨幣支付）</li>
          <li>新文章發布時自動 email 通知訂閱用戶</li>
          <li>其他功能持續開發中</li>
        </ul>
      </section>

      <section>
        <h2>技術架構</h2>
        <ul>
          <li>Docker Compose 部署至 GCP VM，使用 Cloud DNS 管理域名</li>
          <li>Google Cloud Storage (GCS) 作為媒體檔案存儲</li>
          <li>Celery 負責同步 Paddle 用戶資料與寄送 email</li>
          <li>Nginx 反向代理 + acme-companion 自動更新 SSL</li>
          <li>前後端分離：Vue 作為前端，Django REST 提供 API</li>
          <li>響應式網頁設計 (RWD)，支援桌面與行動裝置瀏覽</li>
          <li>支援深色/淺色模式切換</li>
        </ul>
      </section>

      <section>
        <h2>專案連結</h2>
        <p>
          <a href="https://github.com/DimitryW/mySubBlog" target="_blank">
            GitHub Repository
          </a>
        </p>
      </section>
    </div>
    <footer class="footer">
      <div class="footer-inner">
        <img src="/small_site_logo.jpg" alt="Logo" class="footer-logo" />
        <span>© 2025 Dimitry Wu</span>
      </div>
    </footer>
  </div>
</template>


<style scoped>
h1 {
  color: var(--color-text-2);
  height: 100px;
  width: 80%;
  font-weight: 600;
  margin: 0 auto;
  line-height: 100px;
}

.wrapper {
  display: grid;
  grid-template-rows: auto 1fr;
}

.content {
  width: 80%;
  min-height: 800px;
  margin: 0 auto;
  color: var(--color-text-1);
  /* box-shadow: 0 10px 10px 5px rgba(0, 0, 0, 0.1); */
  padding: 3rem 3rem 5rem;
  border-radius: 8px;
  /* background: var(--color-background-strong); */
}

.footer {
  margin-bottom: 1rem;
  padding-top: 1.5rem;
  border-top: 1px solid var(--color-background-highlight-3);
  text-align: center;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.footer-inner {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.footer-logo {
  width: 40px; /* 可依需求調整大小 */
  height: auto;
}

.footer span {
  font-size: 0.9rem;
  color: var(--color-text-2);
}
</style>
