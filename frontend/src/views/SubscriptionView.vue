<script setup>
import { ref, onMounted, computed } from "vue";
import { useUserStore } from '../stores/user'

const userStore = useUserStore()
let paddleCustomerId = computed(() => userStore.user?.paddle_customer_id)

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
  isLoadingPrices.value = true;
  try {
    const result = await Paddle.PricePreview({
      items: [
        { quantity: 1, priceId: CONFIG.prices.tier1[billingCycle.value] },
        { quantity: 1, priceId: CONFIG.prices.tier2[billingCycle.value] }
      ],
      address: { countryCode: country.value }
    });

    result.data.details.lineItems.forEach((item) => {
      const price = item.formattedTotals.subtotal;
      const desc = item.product.description;
      if (item.price.id === CONFIG.prices.tier1[billingCycle.value]) {
        tier1Price.value = price;
        tier1Desc.value = desc;
      } else if (item.price.id === CONFIG.prices.tier2[billingCycle.value]) {
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

function openCheckout(plan) {
  console.log(paddleCustomerId)
  if (!paddleReady || !paddleCustomerId.value) return
  Paddle.Checkout.open({
    items: [{ priceId: CONFIG.prices[plan][billingCycle.value], quantity: 1 }],
    customer: { id: paddleCustomerId.value },
    settings: {
      theme: "light",
      displayMode: "overlay",
      variant: "one-page"
    }
  });
}

onMounted(() => {
  initPaddle();
});
</script>

<template>
  <div class="subscription">
    <h1 class="title">Choose Your Plan</h1>

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
      <div class="plan-card">
        <h3>Tier 1</h3>
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
        <button @click="openCheckout('tier1')">Get started</button>
        <div class="productDesc">
          <span>{{tier1Desc}}</span>
        </div>
      </div>

      <!-- Tier 2 -->
      <div class="plan-card popular">
        <div class="badge">Popular</div>
        <h3>Tier 2</h3>
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
        <button @click="openCheckout('tier2')">Get started</button>
        <div class="productDesc">
          <span>{{tier2Desc}}</span>
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

.title {
  color: var(--color-text-1);
  font-size: 2rem;
  font-weight: bold;
  margin-bottom: 2rem;
}

.billing-toggle {
  margin: 1.5rem;
  height: 3rem;
}

.billing-toggle button {
  color: var(--color-text-3);
  padding: 0.5rem 1rem;
  margin: 0 0.5rem;
  border: 1px solid #ccc;
  background: var(--color-background-soft);
  border: 1px solid var(--color-background-highlight-2);
  cursor: pointer;
}

.billing-toggle button.active {
  background: var(--color-button-highlight-1);
  border: 1px solid var(--color-background-highlight-1);
  color: var(--color-button-text);
  font-weight: 600;
}

.pricing-grid {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 2rem;
}

.plan-card {
  border: 1px solid var(--color-background-highlight-2);
  border-radius: 8px;
  padding: 2rem;
  width: 280px;
  position: relative;
  background: var(--color-background-strong);
  color: var(--color-text-3);
  box-shadow: 0 2px 6px rgba(0,0,0,0.08),
              0 6px 20px rgba(0,0,0,0.12);
}

.plan-card.popular {
  border: 2px solid var(--color-button-highlight-1);
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
}

button {
  padding: 0.75rem 1.5rem;
  border: none;
  background: var(--color-background-highlight-1);
  color: #fff;
  font-weight: 600;
  border-radius: 4px;
  cursor: pointer;
  transition: transform 0.2s ease, box-shadow 0.3s ease;
}

button:hover {
  transform: scale(1.06); 
  box-shadow: inset 0 0 0 2px var(--color-button-highlight-2);
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
