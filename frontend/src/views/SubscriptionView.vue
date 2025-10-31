<script setup>
import { ref, onMounted, computed, watch } from "vue";
import { useRouter, useRoute } from 'vue-router'
import { useUserStore } from '../stores/user'
import { fetchMySubscription } from '@/api/subscription.js'
import { changeSubscription } from '@/api/subscription.js'

const router = useRouter() 
const route = useRoute()
const subscription = ref({});
const currentPriceId = ref('');
const userStore = useUserStore();
const selectedPriceId = ref(''); 
const paddleCustomerId = computed(() => userStore.user?.paddle_customer_id);

const CONFIG = {
  clientToken: import.meta.env.VITE_PADDLE_TOKEN,
  prices: {
    tier1: {
      month: "pri_01k78x871cta18fyfh0ryrqe9j",
      year: "pri_01k78xr398qvzee19150r6qa3p"
    },
    tier2: {
      month: "pri_01k78x6q4qqc678s54caav311c",
      year: "pri_01k78xpgh94fbvxn9w64rzsk1x"
    }
  }
};

const billingCycle = ref("month");
const country = ref("US");
const tier1PriceId = ref("");
const tier2PriceId = ref("");
const tier1Price = ref("$10.00");
const tier2Price = ref("$15.00");
const tier1Desc = ref("");
const tier2Desc = ref("");
const isLoadingPrices = ref(false);
let paddleReady = false;

function initPaddle() {
  if (window.Paddle) {
    Paddle.Environment.set("sandbox");
    Paddle.Initialize({
      token: CONFIG.clientToken,
      eventCallback: (event) => console.log("Paddle event:", event)
    });
    paddleReady = true;
    updatePrices();
  } else {
    console.error("Paddle.js not loaded yet");
  }
}

async function updatePrices() {
  if (!paddleReady) return;
  selectedPriceId.value = '';
  isLoadingPrices.value = true;
  try {
    const result = await Paddle.PricePreview({
      items: [
        { quantity: 1, priceId: CONFIG.prices.tier1[billingCycle.value] },
        { quantity: 1, priceId: CONFIG.prices.tier2[billingCycle.value] }
      ],
      address: { countryCode: country.value }
    });

    console.log(result);

    result.data.details.lineItems.forEach((item) => {
      const priceId = item.price.id;
      const price = item.formattedTotals.subtotal;
      const desc = item.product.description;
      if (priceId === CONFIG.prices.tier1[billingCycle.value]) {
        tier1PriceId.value = priceId;
        tier1Price.value = price;
        tier1Desc.value = desc;
      } else if (priceId === CONFIG.prices.tier2[billingCycle.value]) {
        tier2PriceId.value = priceId;
        tier2Price.value = price;
        tier2Desc.value = desc;
      }
    });
  } catch (err) {
    console.error("Error fetching prices:", err);
  } finally {
    isLoadingPrices.value = false;
  }
}

function updateBillingCycle(cycle) {
  billingCycle.value = cycle;
  updatePrices();
}

function openCheckout(price) {
  console.log('paddleCustomerId: ', paddleCustomerId.value)
  if (!paddleReady || !paddleCustomerId.value) return
  let theme = localStorage.getItem('theme');
  if (!theme) {
    const isDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
    theme = isDark ? "dark" : "light";
  }
  Paddle.Checkout.open({
    items: [{ priceId: price, quantity: 1 }],
    customer: { id: paddleCustomerId.value },
    settings: {
      allowedPaymentMethods: ["card"],
      theme: theme,
      displayMode: "overlay",
      variant: "one-page",
    }
  });
}

async function fetchSubscription() {
  try {
    subscription.value = await fetchMySubscription();
    currentPriceId.value = subscription.value.price_id;
    console.log("My subscription updated:", subscription.value);
  } catch (err) {
    console.error("Failed to fetch subscription:", err);
  }
}

onMounted(() => {
  initPaddle();
  fetchSubscription();
});

watch(
  () => route.fullPath,
  async () => {
    if (route.path === "/subscription") {
      fetchSubscription();
    }
  },
  { immediate: true } // 元件一載入就抓一次
);

const isSwitching = ref(false);

async function handleSwitchPlan(newPriceId) {
  if (isSwitching.value) return;
  isSwitching.value = true;

  try {
    await changeSubscription(subscription.value.id, newPriceId);
    // 成功跳轉到成功頁
    router.push({ name: 'subscription-success' });
  } catch (err) {
    console.error("Failed to switch plan:", err);
    alert("Failed to switch subscription.");
  } finally {
    isSwitching.value = false;
  }
}
</script>

<template>
  <div class="subscription">
    

    <div>
      <h1 class="title">Current Subscription</h1>
      <div v-if="!subscription.name" class="subscription-card">
        You have no active subscription.
      </div>
      <div v-else class="subscription-card">
        <h2>{{ subscription.name }}</h2>
        <p>{{ subscription.desc }}</p>
        <hr />
        <h3>Payment Detail</h3>
        <p>Price: ${{ subscription.price }}</p>
        <p>Next payment: {{ subscription.next_payment }}</p>
        <p>Status: {{ subscription.status }}</p>
      </div>

      <h1 v-if="!subscription.name" class="title">Upgrade Your Plan</h1>
      <h1 v-else class="title">Change Your Plan</h1>
      <!-- Billing Toggle -->
      <div class="billing-toggle">
        <button
          :class="{ active: billingCycle === 'month' }"
          @click="updateBillingCycle('month')"
        >
          Monthly
        </button>
        <button
          :class="{ active: billingCycle === 'year' }"
          @click="updateBillingCycle('year')"
        >
          Yearly (Save Up to 16%)
        </button>
      </div>

      <!-- Pricing Grid -->
      <div class="pricing-grid">
        <!-- Tier 1 -->
        <div class="plan-card" :class="{ selected: selectedPriceId && selectedPriceId === tier1PriceId }" @click="selectedPriceId = tier1PriceId">
          <h3 class="tier">Tier 1<p class="current-plan" v-if="currentPriceId === tier1PriceId">current</p></h3>
          <div class="price">
            <span class="amount">
              <template v-if="isLoadingPrices">
                <span class="spinner"></span>
              </template>
              <template v-else>
                {{ tier1Price }}
              </template>
            </span>
            <span class="cycle">/ {{ billingCycle }}</span>
          </div>
          <!-- <button v-if="!subscription.name" @click="openCheckout('tier1')">Get Started</button>
          <button :disabled="isSwitching" v-else-if="currentPriceId !== tier1PriceId" @click="handleSwitchPlan(tier1PriceId)">
          <template v-if="isSwitching">
          <span class="spinner"></span> Switching...
          </template>
          <template v-else>
            Switch Plan
          </template>
          </button> -->
          <!-- <p v-if="currentPriceId === tier1PriceId" class="current-plan">Current Plan</p> -->
          <div class="productDesc">
            <span>{{tier1Desc}}</span>
          </div>
        </div>

        <!-- Tier 2 -->
        <div class="plan-card popular" :class="{ selected: selectedPriceId && selectedPriceId === tier2PriceId }" @click="selectedPriceId = tier2PriceId">
          <!-- <div class="badge">Popular</div> -->
          <h3 class="tier">Tier 2<p class="current-plan" v-if="currentPriceId === tier2PriceId">current</p></h3>
          <div class="price">
            <span class="amount">
              <template v-if="isLoadingPrices">
                <span class="spinner"></span>
              </template>
              <template v-else>
                {{ tier2Price }}
              </template>
            </span>
            <span class="cycle">/ {{ billingCycle }}</span>
          </div>
          <!-- <button v-if="!subscription.name" @click="openCheckout('tier2')">Get Started</button>
          <button :disabled="isSwitching" v-else-if="currentPriceId !== tier2PriceId" @click="handleSwitchPlan(tier2PriceId)">
          <template v-if="isSwitching">
          <span class="spinner"></span> Switching...
          </template>
          <template v-else>
            Switch Plan
          </template>
          </button> -->
          <!-- <p v-if="currentPriceId === tier2PriceId" class="current-plan">Current Plan</p> -->
          <div class="productDesc">
            <span>{{tier2Desc}}</span>
          </div>
        </div>

      </div>

      <div class="switch-btn-wrapper">
        <div v-if="selectedPriceId && currentPriceId !== selectedPriceId">
          <button v-if="!subscription.name" @click="openCheckout(selectedPriceId)">
              Get Started
          </button>

          <button v-else :disabled="isSwitching" @click="handleSwitchPlan(selectedPriceId)">
            <template v-if="isSwitching">
              <span class="spinner"></span> Switching...
            </template>
            <template v-else>
              Switch Plan
            </template>
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.subscription {
  min-height: 100vh;
  padding: 2rem;
  text-align: center;
}

.subscription-card {
  /* width: 80%; */
  max-width: 800px;
  margin: 0 auto 3rem;
  padding: 2rem 4rem;
  max-height: 1200px;
  background: var(--color-background-strong);
  border: 1px solid var(--color-background-highlight-1);
  border-radius: 8px;
  /* box-shadow: 0 2px 6px rgba(0,0,0,0.1); */
  color: var(--color-text-1);
  text-align: left;           /* 卡片內容靠左對齊 */
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.title {
  color: var(--color-text-2);
  font-size: 2rem;
  font-weight: 600;
  margin-bottom: 1.5rem;
}

.tier {
  display: flex;
  justify-content: center;
  font-weight: 600;
}

hr {
  border: 0; 
  border-top: 1px solid var(--color-background-highlight-3); 
  margin: 0.5rem 0;
  }


.billing-toggle {
  height: 3rem;
}

.billing-toggle button {
  color: var(--color-text-3);
  padding: 0.5rem 1rem;
  margin: 0 0.5rem;
  background: var(--color-background-soft);
  border: 1px solid var(--color-background-highlight-2);
  cursor: pointer;
}

.billing-toggle button.active {
  border: 2px solid var(--color-button-highlight-1);
  color: var(--color-text-1);
  font-weight: 600;
}

.pricing-grid {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 1rem 5rem;
}

.plan-card {
  border: 1px solid var(--color-background-highlight-1);
  border-radius: 8px;
  padding: 2rem;
  margin: 1rem 0 2.5rem;
  width: 320px;
  position: relative;
  background: var(--color-background-soft);
  color: var(--color-text-3);
  cursor: pointer;
}

.plan-card.selected {
  border: 2px solid var(--color-button-highlight-1);
  box-shadow: 0 2px 6px rgba(0,0,0,0.08),
              0 6px 20px rgba(0,0,0,0.12);
}

.plan-card.popular {
  /* border: 2px solid var(--color-button-highlight-1); */
}

.plan-card .badge {
  position: absolute;
  top: -1rem;
  right: 20px;
  background: var(--color-button-highlight-1);
  color: var(--color-button-text);
  padding: 0.25rem 0.75rem;
  border-radius: 999px;
  font-size: 0.8rem;
  font-weight: 600;
}

.price {
  margin: 1rem 0;
  font-size: 1.5rem;
}

.productDesc {
  margin: 1rem;
  color: var(--color-text-1);
  white-space: pre-wrap;
}

.switch-btn-wrapper {
  height: 3rem;
}

.switch-btn-wrapper button div {
  font-weight: 600;
}

button {
  padding: 0.75rem 1.5rem;
  border: none;
  background: var(--color-background-highlight-1);
  color: #fff;
  font-size: 15px;
  font-weight: 600;
  border-radius: 4px;
  cursor: pointer;
  transition: transform 0.2s ease, box-shadow 0.3s ease;
}

button:hover {
  transform: scale(1.06); 
}

.current-plan {
  position: absolute;
  top: 0.5rem;
  left: 10px;
  margin: 0 auto;
  padding: 0 1rem;
  border: none;
  background: var(--color-background-highlight-3);
  color: var(--color-text-3);
  font-size: 0.8rem;
  font-weight: 600;
  border-radius: 999px;
  transition: transform 0.2s ease, box-shadow 0.3s ease;
}

.spinner {
  display: inline-block;
  width: 18px;
  height: 18px;
  border: 3px solid #efefefff;
  border-top: 3px solid var(--color-button-highlight-2);
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
  vertical-align: middle;
  margin-right: 1rem;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}
</style>
