<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const authStore = useAuthStore()

const userType = ref('volunteer')
const email = ref('')
const password = ref('')
const showPassword = ref(false)
const isLoading = ref(false)
const errorMessage = ref('')

const togglePasswordVisibility = () => {
  showPassword.value = !showPassword.value
}

const handleSubmit = async () => {
  if (!email.value || !password.value) {
    errorMessage.value = 'Пожалуйста, заполните все поля'
    return
  }

  try {
    isLoading.value = true
    errorMessage.value = ''

    if (userType.value === 'volunteer') {
      await authStore.loginVolunteer(email.value, password.value)
    } else {
      await authStore.loginVeteran(email.value, password.value)
    }

    const redirectPath = userType.value === 'volunteer' ? '/home/volunteer' : '/home/veteran'
    router.push(redirectPath)
  } catch (error) {
    errorMessage.value = error.message || 'Ошибка авторизации. Проверьте данные и попробуйте снова.'
  } finally {
    isLoading.value = false
  }
}
</script>

<template>
  <div class="bg-[#F5F8FF] relative h-screen">
    <div
      class="absolute top-1/2 left-1/2 -translate-1/2 shadow-lg w-120 flex flex-col gap-y-7.5 p-10 bg-white rounded-[20px]"
    >
      <h2 class="text-4xl font-semibold tracking-[0.5%] text-center text-[#1F2937]">Вход</h2>

      <div class="flex">
        <!-- Волонтер -->
        <label class="flex-1 w-1/2 cursor-pointer">
          <input type="radio" v-model="userType" value="volunteer" class="hidden peer" />
          <div
            class="p-2.5 text-[#1F2937] text-center text-[15px] font-semibold tracking-[0.5%] bg-[#F3F4F6] rounded-l-lg peer-checked:border peer-checked:border-[#E5E7EB] peer-checked:shadow-sm peer-checked:bg-white"
          >
            Волонтер
          </div>
        </label>

        <!-- Ветеран -->
        <label class="flex-1 w-1/2 cursor-pointer">
          <input type="radio" v-model="userType" value="veteran" class="hidden peer" />
          <div
            class="p-2.5 text-[#1F2937] text-center text-[15px] font-semibold tracking-[0.5%] bg-[#F3F4F6] rounded-r-lg peer-checked:border peer-checked:border-[#E5E7EB] peer-checked:shadow-sm peer-checked:bg-white"
          >
            Ветеран
          </div>
        </label>
      </div>

      <!-- Остальная форма -->
      <form @submit.prevent="handleSubmit" class="flex flex-col gap-y-5">
        <div class="flex flex-col gap-y-2.5">
          <label class="flex flex-col gap-y-2.5">
            <span class="mb-2.5 text-sm font-semibold text-[#1F2937] tracking-[0.5%]">Почта</span>
            <input
              v-model="email"
              type="email"
              class="w-full px-4 py-2.5 border border-[#E5E7EB] rounded-lg shadow-sm focus:border-[#2563EB] focus:ring-2 focus:ring-[#2563EB]/20"
          /></label>

          <label class="flex flex-col gap-y-2.5"
            ><span class="mb-2.5 text-sm font-semibold text-[#1F2937] tracking-[0.5%]">Пароль</span>
            <div class="relative mt-2.5">
              <input
                v-model="password"
                :type="showPassword ? 'text' : 'password'"
                class="w-full px-4 py-2 border border-[#E5E7EB] rounded-lg shadow-sm focus:border-[#2563EB] focus:ring-2 focus:ring-[#2563EB]/20"
              />
              <button
                type="button"
                @click="togglePasswordVisibility"
                class="absolute inset-y-0 right-0 pr-3 flex items-center text-sm leading-5"
              >
                <svg
                  v-if="!showPassword"
                  width="16"
                  height="16"
                  viewBox="0 0 16 16"
                  fill="none"
                  xmlns="http://www.w3.org/2000/svg"
                >
                  <g clip-path="url(#clip0_27_657)">
                    <path
                      d="M6.58669 6.58667C6.39019 6.76977 6.23259 6.99057 6.12327 7.2359C6.01396 7.48123 5.95518 7.74607 5.95045 8.01461C5.94571 8.28315 5.99511 8.54989 6.0957 8.79893C6.19629 9.04796 6.346 9.27419 6.53592 9.46411C6.72584 9.65402 6.95206 9.80374 7.2011 9.90433C7.45013 10.0049 7.71688 10.0543 7.98542 10.0496C8.25396 10.0448 8.51879 9.98606 8.76412 9.87675C9.00946 9.76744 9.23026 9.60983 9.41336 9.41334"
                      stroke="#6B7280"
                      stroke-linecap="round"
                      stroke-linejoin="round"
                    />
                    <path
                      d="M7.15332 3.38668C7.43419 3.35168 7.71694 3.33387 7.99999 3.33334C12.6667 3.33334 14.6667 8.00001 14.6667 8.00001C14.3686 8.63809 13.9948 9.23797 13.5533 9.78668"
                      stroke="#6B7280"
                      stroke-linecap="round"
                      stroke-linejoin="round"
                    />
                    <path
                      d="M4.40665 4.40668C3.08081 5.30976 2.01989 6.55018 1.33331 8.00001C1.33331 8.00001 3.33331 12.6667 7.99998 12.6667C9.27725 12.6701 10.5272 12.2967 11.5933 11.5933"
                      stroke="#6B7280"
                      stroke-linecap="round"
                      stroke-linejoin="round"
                    />
                    <path
                      d="M1.33331 1.33334L14.6666 14.6667"
                      stroke="#6B7280"
                      stroke-linecap="round"
                      stroke-linejoin="round"
                    />
                  </g>
                  <defs>
                    <clipPath id="clip0_27_657">
                      <rect width="16" height="16" fill="white" />
                    </clipPath>
                  </defs>
                </svg>

                <svg
                  v-else
                  width="16"
                  height="16"
                  viewBox="0 0 16 16"
                  fill="none"
                  xmlns="http://www.w3.org/2000/svg"
                >
                  <path
                    d="M1.33334 8.00001C1.33334 8.00001 3.33334 3.33334 8 3.33334C12.6667 3.33334 14.6667 8.00001 14.6667 8.00001C14.6667 8.00001 12.6667 12.6667 8 12.6667C3.33334 12.6667 1.33334 8.00001 1.33334 8.00001Z"
                    stroke="#6B7280"
                    stroke-linecap="round"
                    stroke-linejoin="round"
                  />
                  <path
                    d="M8 10C9.10457 10 10 9.10457 10 8C10 6.89543 9.10457 6 8 6C6.89543 6 6 6.89543 6 8C6 9.10457 6.89543 10 8 10Z"
                    stroke="#6B7280"
                    stroke-linecap="round"
                    stroke-linejoin="round"
                  />
                </svg>
              </button>
            </div>
          </label>
        </div>

        <!-- Сообщение об ошибке -->
        <div v-if="errorMessage" class="text-red-500 text-sm">
          {{ errorMessage }}
        </div>

        <div class="flex justify-between pt-2.5">
          <router-link to="/auth/register">
            <button
              type="button"
              class="px-4 py-2 border border-[#2563EB] text-[#2563EB] rounded-lg text-[15px] font-semibold tracking-[0.5%]"
            >
              Зарегистрироваться
            </button>
          </router-link>
          <button
            type="submit"
            :disabled="isLoading"
            class="px-4 py-2 bg-[#2563EB] text-white rounded-lg text-[15px] font-semibold tracking-[0.5%] hover:bg-[#1D4ED8] disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
          >
            <span v-if="!isLoading">Войти</span>
            <span v-else>Вход...</span>
          </button>
        </div>
      </form>
    </div>
  </div>
</template>
