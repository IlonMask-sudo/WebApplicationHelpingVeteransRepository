<script setup>
import { computed, ref } from 'vue'

// Состояние для хранения списка заявок
const requests = ref([
  {
    id: 1,
    title: 'Нужна помощь с переездом',
    type: 'transport',
    description: 'Требуется грузовик для переезда 15 числа',
    location: 'Москва, ул. Ленина 10',
    createdAt: new Date().toLocaleString(),
    status: 'active',
  },
  {
    id: 2,
    title: 'Требуются лекарства',
    type: 'medicine',
    description: 'Нужны лекарства для пожилого человека',
    location: 'Санкт-Петербург, ул. Пушкина 5',
    createdAt: new Date(Date.now() - 86400000).toLocaleString(),
    status: 'in_progress',
  },
  {
    id: 3,
    title: 'Продукты первой необходимости',
    type: 'food',
    description: 'Нужны продукты для семьи из 4 человек',
    location: 'Казань, ул. Гоголя 15',
    createdAt: new Date(Date.now() - 172800000).toLocaleString(),
    status: 'canceled',
  },
  {
    id: 4,
    title: 'Помощь с ремонтом',
    type: 'other',
    description: 'Требуется помощь с ремонтом квартиры',
    location: 'Новосибирск, ул. Советская 20',
    createdAt: new Date(Date.now() - 259200000).toLocaleString(),
    status: 'completed',
  },
  {
    id: 5,
    title: 'Транспорт для доставки',
    type: 'transport',
    description: 'Нужен транспорт для доставки гуманитарной помощи',
    location: 'Екатеринбург, ул. Мира 8',
    createdAt: new Date(Date.now() - 345600000).toLocaleString(),
    status: 'completed',
  },
  {
    id: 6,
    title: 'Медицинская консультация',
    type: 'medicine',
    description: 'Требуется консультация врача',
    location: 'Ростов-на-Дону, ул. Красноармейская 3',
    createdAt: new Date(Date.now() - 432000000).toLocaleString(),
    status: 'in_progress',
  },
  {
    id: 7,
    title: 'Медицинская консультация',
    type: 'medicine',
    description: 'Требуется консультация врача',
    location: 'Ростов-на-Дону, ул. Красноармейская 3',
    createdAt: new Date(Date.now() - 432000000).toLocaleString(),
    status: 'in_progress',
  },
])

// Состояние для формы
const form = ref({
  title: '',
  type: '',
  description: '',
  location: '',
})

// Состояние модальных окон
const showModal = ref(false)
const showViewModal = ref(false)
const currentRequest = ref(null)
const isEditing = ref(false)

// Состояние для отображения всех заявок
const showAllActive = ref(false)
const showAllInProgress = ref(false)
const showAllCanceled = ref(false)
const showAllCompleted = ref(false)

// Цвета и тексты для статусов
const statusConfig = {
  active: {
    text: 'Активная',
    color: '#D1FAE5',
    textColor: '#065F46',
  },
  in_progress: {
    text: 'В работе',
    color: '#DBEAFE',
    textColor: '#1E40AF',
  },
  canceled: {
    text: 'Отозвана',
    color: '#FEE2E2',
    textColor: '#991B1B',
  },
  completed: {
    text: 'Завершена',
    color: '#DBFEDB',
    textColor: '#1EAF53',
  },
}

// Фильтрация заявок
const activeRequests = computed(() => {
  return requests.value
    .filter((request) => request.status === 'active')
    .sort((a, b) => new Date(b.createdAt) - new Date(a.createdAt))
})

const inProgressRequests = computed(() => {
  return requests.value
    .filter((request) => request.status === 'in_progress')
    .sort((a, b) => new Date(b.createdAt) - new Date(a.createdAt))
})

const canceledRequests = computed(() => {
  return requests.value
    .filter((request) => request.status === 'canceled')
    .sort((a, b) => new Date(b.createdAt) - new Date(a.createdAt))
})

const completedRequests = computed(() => {
  return requests.value
    .filter((request) => request.status === 'completed')
    .sort((a, b) => new Date(b.createdAt) - new Date(a.createdAt))
})

// Отображение только 4 последних заявок
const displayedActiveRequests = computed(() => {
  return showAllActive.value ? [...activeRequests.value] : activeRequests.value.slice(0, 4)
})

const displayedInProgressRequests = computed(() => {
  return showAllInProgress.value
    ? [...inProgressRequests.value]
    : inProgressRequests.value.slice(0, 4)
})

const displayedCanceledRequests = computed(() => {
  return showAllCanceled.value ? [...canceledRequests.value] : canceledRequests.value.slice(0, 4)
})

const displayedCompletedRequests = computed(() => {
  return showAllCompleted.value ? [...completedRequests.value] : completedRequests.value.slice(0, 4)
})

// Создание новой заявки
const createRequest = () => {
  if (!form.value.title || !form.value.type) {
    alert('Заполните обязательные поля')
    return
  }

  const newRequest = {
    id: Date.now(),
    title: form.value.title,
    type: form.value.type,
    description: form.value.description,
    location: form.value.location,
    createdAt: new Date().toLocaleString(),
    status: 'active',
  }

  requests.value.unshift(newRequest)
  resetForm()
  showModal.value = false
}

// Открытие заявки для редактирования
const openRequest = (request) => {
  currentRequest.value = { ...request }
  isEditing.value = false
  showViewModal.value = true
}

// Обновление заявки
const updateRequest = () => {
  const index = requests.value.findIndex((r) => r.id === currentRequest.value.id)
  if (index !== -1) {
    requests.value[index] = { ...currentRequest.value }
  }
  isEditing.value = false
}

// Сброс формы
const resetForm = () => {
  form.value = {
    title: '',
    type: '',
    description: '',
    location: '',
  }
}

// Изменение статуса заявки
const changeStatus = (request, newStatus) => {
  const index = requests.value.findIndex((r) => r.id === request.id)
  if (index !== -1) {
    requests.value[index].status = newStatus
  }
  showViewModal.value = false
}
</script>

<template>
  <section class="px-10 pt-25">
    <!-- Секция активных заявок -->
    <div class="mb-12">
      <div class="flex justify-between items-center pb-5">
        <h3 class="font-semibold tracking-[0.5%] text-[#1F2937] text-[32px]">Активные заявки</h3>
        <button
          type="button"
          class="py-2.5 px-4 text-white bg-[#2563EB] rounded-lg text-[15px] font-semibold tracking-[0.5%]"
          @click="showModal = true"
        >
          Создать заявку
        </button>
      </div>

      <!-- Список активных заявок -->
      <div class="flex gap-5 flex-wrap pb-5">
        <div
          v-for="request in displayedActiveRequests"
          :key="request.id"
          class="w-full md:w-[calc(50%-10px)] p-5 bg-white rounded-lg flex flex-col gap-y-4 shadow-sm border border-[#E5E7EB] cursor-pointer hover:shadow-md transition-shadow"
          @click="openRequest(request)"
        >
          <div class="flex justify-between items-start">
            <div>
              <h4 class="text-lg font-bold text-[#1F2937] tracking-[0.5%]">{{ request.title }}</h4>
              <div class="mt-3 text-xs text-[#9CA3AF]">Создано: {{ request.createdAt }}</div>
            </div>
            <span
              class="px-2.5 py-1.5 text-xs font-medium rounded-full tracking-[0.5%]"
              :style="{
                backgroundColor: statusConfig[request.status].color,
                color: statusConfig[request.status].textColor,
              }"
            >
              {{ statusConfig[request.status].text }}
            </span>
          </div>
          <p class="text-[#6B7280]">{{ request.description }}</p>
          <button class="flex gap-x-2.5 items-center px-4 py-3.5">
            <span class="font-semibold text-[15px] tracking-[0.5%] text-[#3B82F6]">Подробнее</span>
            <svg
              width="6"
              height="8"
              viewBox="0 0 6 8"
              fill="none"
              xmlns="http://www.w3.org/2000/svg"
            >
              <path
                d="M1.25 7.5L4.75 4L1.25 0.5"
                stroke="#2563EB"
                stroke-linecap="round"
                stroke-linejoin="round"
              />
            </svg>
          </button>
        </div>
      </div>

      <!-- Кнопка "Все" для активных заявок -->
      <div class="flex justify-end mt-5" v-if="activeRequests.length >= 4">
        <button
          @click="showAllActive = !showAllActive"
          class="px-4 py-2 text-[#2563EB] border border-[#2563EB] rounded-lg hover:bg-[#2563EB] hover:text-white transition-colors"
        >
          {{ showAllActive ? 'Скрыть' : 'Все' }}
        </button>
      </div>
      <div v-if="activeRequests.length === 0" class="text-center py-4 text-gray-500">
        Нет активных заявок
      </div>
    </div>

    <!-- Секция заявок в работе -->
    <div class="mb-12">
      <div class="flex justify-between items-center pb-5">
        <h3 class="font-semibold tracking-[0.5%] text-[#1F2937] text-[32px]">Заявки в работе</h3>
      </div>

      <!-- Список заявок в работе -->
      <div class="flex gap-5 flex-wrap pb-5">
        <div
          v-for="request in displayedInProgressRequests"
          :key="request.id"
          class="w-full md:w-[calc(50%-10px)] p-5 bg-white rounded-lg flex flex-col gap-y-4 shadow-sm border border-[#E5E7EB] cursor-pointer hover:shadow-md transition-shadow"
          @click="openRequest(request)"
        >
          <div class="flex justify-between items-start">
            <div>
              <h4 class="text-lg font-bold text-[#1F2937] tracking-[0.5%]">{{ request.title }}</h4>
              <div class="mt-3 text-xs text-[#9CA3AF]">Создано: {{ request.createdAt }}</div>
            </div>
            <span
              class="px-2.5 py-1.5 text-xs font-medium rounded-full tracking-[0.5%]"
              :style="{
                backgroundColor: statusConfig[request.status].color,
                color: statusConfig[request.status].textColor,
              }"
            >
              {{ statusConfig[request.status].text }}
            </span>
          </div>
          <p class="text-[#6B7280]">{{ request.description }}</p>
          <button class="flex gap-x-2.5 items-center px-4 py-3.5">
            <span class="font-semibold text-[15px] tracking-[0.5%] text-[#3B82F6]">Подробнее</span>
            <svg
              width="6"
              height="8"
              viewBox="0 0 6 8"
              fill="none"
              xmlns="http://www.w3.org/2000/svg"
            >
              <path
                d="M1.25 7.5L4.75 4L1.25 0.5"
                stroke="#2563EB"
                stroke-linecap="round"
                stroke-linejoin="round"
              />
            </svg>
          </button>
        </div>
      </div>

      <!-- Кнопка "Все" для заявок в работе -->
      <div class="flex justify-end mt-5" v-if="inProgressRequests.length >= 4">
        <button
          @click="showAllInProgress = !showAllInProgress"
          class="px-4 py-2 text-[#2563EB] border border-[#2563EB] rounded-lg hover:bg-[#2563EB] hover:text-white transition-colors"
        >
          {{ showAllInProgress ? 'Скрыть' : 'Все' }}
        </button>
      </div>
      <div v-if="inProgressRequests.length === 0" class="text-center py-4 text-gray-500">
        Нет заявок в работе
      </div>
    </div>

    <!-- Секция архива заявок -->
    <div class="mb-12">
      <div class="flex justify-between items-center pb-5">
        <h3 class="font-semibold tracking-[0.5%] text-[#1F2937] text-[32px]">Архив заявок</h3>
      </div>

      <!-- Подсекция отозванных заявок -->
      <div class="mb-8">
        <h4 class="text-xl font-semibold pb-2.5">Отозванные заявки</h4>
        <div class="flex gap-5 flex-wrap pb-5">
          <div
            v-for="request in displayedCanceledRequests"
            :key="request.id"
            class="w-full md:w-[calc(50%-10px)] p-5 bg-white rounded-lg flex flex-col gap-y-4 shadow-sm border border-[#E5E7EB] cursor-pointer hover:shadow-md transition-shadow"
            @click="openRequest(request)"
          >
            <div class="flex justify-between items-start">
              <div>
                <h4 class="text-lg font-bold text-[#1F2937] tracking-[0.5%]">
                  {{ request.title }}
                </h4>
                <div class="mt-3 text-xs text-[#9CA3AF]">Создано: {{ request.createdAt }}</div>
              </div>
              <span
                class="px-2.5 py-1.5 text-xs font-medium rounded-full tracking-[0.5%]"
                :style="{
                  backgroundColor: statusConfig[request.status].color,
                  color: statusConfig[request.status].textColor,
                }"
              >
                {{ statusConfig[request.status].text }}
              </span>
            </div>
            <p class="text-[#6B7280]">{{ request.description }}</p>
            <button class="flex gap-x-2.5 items-center px-4 py-3.5">
              <span class="font-semibold text-[15px] tracking-[0.5%] text-[#3B82F6]"
                >Подробнее</span
              >
              <svg
                width="6"
                height="8"
                viewBox="0 0 6 8"
                fill="none"
                xmlns="http://www.w3.org/2000/svg"
              >
                <path
                  d="M1.25 7.5L4.75 4L1.25 0.5"
                  stroke="#2563EB"
                  stroke-linecap="round"
                  stroke-linejoin="round"
                />
              </svg>
            </button>
          </div>
        </div>

        <!-- Кнопка "Все" для отозванных заявок -->
        <div class="flex justify-end mt-5" v-if="canceledRequests.length >= 4">
          <button
            @click="showAllCanceled = !showAllCanceled"
            class="px-4 py-2 text-[#2563EB] border border-[#2563EB] rounded-lg hover:bg-[#2563EB] hover:text-white transition-colors"
          >
            {{ showAllCanceled ? 'Скрыть' : 'Все' }}
          </button>
        </div>
        <div v-if="canceledRequests.length === 0" class="text-center py-4 text-gray-500">
          Нет отозванных заявок
        </div>
      </div>

      <!-- Подсекция завершенных заявок -->
      <div class="mb-8">
        <h4 class="text-xl font-semibold pb-2.5">Завершенные заявки</h4>
        <div class="flex gap-5 flex-wrap pb-5">
          <div
            v-for="request in displayedCompletedRequests"
            :key="request.id"
            class="w-full md:w-[calc(50%-10px)] p-5 bg-white rounded-lg flex flex-col gap-y-4 shadow-sm border border-[#E5E7EB] cursor-pointer hover:shadow-md transition-shadow"
            @click="openRequest(request)"
          >
            <div class="flex justify-between items-start">
              <div>
                <h4 class="text-lg font-bold text-[#1F2937] tracking-[0.5%]">
                  {{ request.title }}
                </h4>
                <div class="mt-3 text-xs text-[#9CA3AF]">Создано: {{ request.createdAt }}</div>
              </div>
              <span
                class="px-2.5 py-1.5 text-xs font-medium rounded-full tracking-[0.5%]"
                :style="{
                  backgroundColor: statusConfig[request.status].color,
                  color: statusConfig[request.status].textColor,
                }"
              >
                {{ statusConfig[request.status].text }}
              </span>
            </div>
            <p class="text-[#6B7280]">{{ request.description }}</p>
            <button class="flex gap-x-2.5 items-center px-4 py-3.5">
              <span class="font-semibold text-[15px] tracking-[0.5%] text-[#3B82F6]"
                >Подробнее</span
              >
              <svg
                width="6"
                height="8"
                viewBox="0 0 6 8"
                fill="none"
                xmlns="http://www.w3.org/2000/svg"
              >
                <path
                  d="M1.25 7.5L4.75 4L1.25 0.5"
                  stroke="#2563EB"
                  stroke-linecap="round"
                  stroke-linejoin="round"
                />
              </svg>
            </button>
          </div>
        </div>

        <!-- Кнопка "Все" для завершенных заявок -->
        <div class="flex justify-end mt-5" v-if="completedRequests.length >= 4">
          <button
            @click="showAllCompleted = !showAllCompleted"
            class="px-4 py-2 text-[#2563EB] border border-[#2563EB] rounded-lg hover:bg-[#2563EB] hover:text-white transition-colors"
          >
            {{ showAllCompleted ? 'Скрыть' : 'Все' }}
          </button>
        </div>
        <div v-if="completedRequests.length === 0" class="text-center py-4 text-gray-500">
          Нет завершенных заявок
        </div>
      </div>
    </div>

    <!-- Модальное окно создания -->
    <div
      v-if="showModal"
      class="fixed inset-0 z-50 overflow-y-auto bg-black/50 flex items-center justify-center"
    >
      <div class="bg-white rounded-[20px] p-10 shadow-lg max-w-2xl w-full mx-4 relative">
        <button
          @click="showModal = false"
          class="absolute top-4 right-4 text-gray-500 hover:text-gray-700"
        >
          <svg
            xmlns="http://www.w3.org/2000/svg"
            class="h-6 w-6"
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
          >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2"
              d="M6 18L18 6M6 6l12 12"
            />
          </svg>
        </button>
        <h2 class="text-4xl font-semibold tracking-[0.5%] text-center text-[#1F2937] pb-7.5">
          Создание заявки о помощи
        </h2>

        <form @submit.prevent="createRequest" class="flex flex-col gap-y-2.5">
          <div class="flex flex-col gap-y-2.5">
            <div class="flex flex-col gap-y-2.5">
              <label class="block text-sm font-semibold text-[#1F2937] tracking-[0.5%]">
                Тема заявки
              </label>
              <input
                v-model="form.title"
                type="text"
                required
                class="w-full px-4 py-2.5 border border-[#E5E7EB] rounded-lg shadow-sm focus:border-[#2563EB] focus:ring-2 focus:ring-[#2563EB]/20"
              />
            </div>

            <div class="flex flex-col gap-y-2.5">
              <label class="block text-sm font-semibold text-[#1F2937] tracking-[0.5%]">
                Тип помощи
              </label>
              <select
                v-model="form.type"
                required
                class="w-full px-4 py-2.5 border border-[#E5E7EB] rounded-lg shadow-sm focus:border-[#2563EB] focus:ring-2 focus:ring-[#2563EB]/20"
              >
                <option value="" disabled selected>Выберите тип помощи</option>
                <option value="transport">Транспорт</option>
                <option value="food">Продукты</option>
                <option value="medicine">Лекарства</option>
                <option value="other">Другое</option>
              </select>
            </div>

            <div class="flex flex-col gap-y-2.5">
              <label class="block text-sm font-semibold text-[#1F2937] tracking-[0.5%]">
                Описание
              </label>
              <textarea
                v-model="form.description"
                rows="5"
                class="w-full px-4 py-2.5 border border-[#E5E7EB] rounded-lg shadow-sm focus:border-[#2563EB] focus:ring-2 focus:ring-[#2563EB]/20 resize-none"
              ></textarea>
            </div>

            <div class="flex flex-col gap-y-2.5">
              <label class="block text-sm font-semibold text-[#1F2937] tracking-[0.5%]">
                Местоположение
              </label>
              <input
                v-model="form.location"
                type="text"
                class="w-full px-4 py-2.5 border border-[#E5E7EB] rounded-lg shadow-sm focus:border-[#2563EB] focus:ring-2 focus:ring-[#2563EB]/20"
              />
            </div>
          </div>

          <div class="flex justify-between pt-4">
            <button
              type="button"
              @click="showModal = false"
              class="px-4 py-2 border border-[#2563EB] text-[#2563EB] rounded-lg text-[15px] font-semibold tracking-[0.5%] hover:bg-[#EFF6FF]"
            >
              Отменить
            </button>
            <button
              type="submit"
              class="px-4 py-2 bg-[#2563EB] text-white rounded-lg text-[15px] font-semibold tracking-[0.5%] hover:bg-[#1D4ED8] disabled:opacity-50 transition-colors"
            >
              Создать
            </button>
          </div>
        </form>
      </div>
    </div>

    <!-- Модальное окно редактирования -->
    <div
      v-if="showViewModal"
      class="fixed inset-0 z-50 overflow-y-auto bg-black/50 flex items-center justify-center"
    >
      <div class="bg-white rounded-[20px] p-10 shadow-lg max-w-2xl w-full mx-4 relative">
        <button
          @click="showViewModal = false"
          class="absolute top-4 right-4 text-gray-500 hover:text-gray-700"
        >
          <svg
            xmlns="http://www.w3.org/2000/svg"
            class="h-6 w-6"
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
          >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2"
              d="M6 18L18 6M6 6l12 12"
            />
          </svg>
        </button>
        <h2 class="text-4xl font-semibold tracking-[0.5%] text-center text-[#1F2937] pb-7.5">
          {{ isEditing ? 'Редактирование заявки' : 'Заявка' }}
        </h2>

        <form @submit.prevent="updateRequest" class="flex flex-col gap-y-2.5">
          <div class="flex flex-col gap-y-2.5">
            <label class="block text-sm font-semibold text-[#1F2937] tracking-[0.5%]">
              Тема заявки
            </label>
            <input
              v-model="currentRequest.title"
              type="text"
              required
              :readonly="!isEditing"
              :class="{ 'bg-gray-100': !isEditing }"
              class="w-full px-4 py-2.5 border border-[#E5E7EB] rounded-lg shadow-sm focus:border-[#2563EB] focus:ring-2 focus:ring-[#2563EB]/20"
            />
          </div>

          <div class="flex flex-col gap-y-2.5">
            <label class="block text-sm font-semibold text-[#1F2937] tracking-[0.5%]">
              Тип помощи
            </label>
            <select
              v-model="currentRequest.type"
              required
              :disabled="!isEditing"
              :class="{ 'bg-gray-100': !isEditing }"
              class="w-full px-4 py-2.5 border border-[#E5E7EB] rounded-lg shadow-sm focus:border-[#2563EB] focus:ring-2 focus:ring-[#2563EB]/20"
            >
              <option value="transport">Транспорт</option>
              <option value="food">Продукты</option>
              <option value="medicine">Лекарства</option>
              <option value="other">Другое</option>
            </select>
          </div>

          <div class="flex flex-col gap-y-2.5">
            <label class="block text-sm font-semibold text-[#1F2937] tracking-[0.5%]">
              Описание
            </label>
            <textarea
              v-model="currentRequest.description"
              rows="5"
              :readonly="!isEditing"
              :class="{ 'bg-gray-100': !isEditing }"
              class="w-full px-4 py-2.5 border border-[#E5E7EB] rounded-lg shadow-sm focus:border-[#2563EB] focus:ring-2 focus:ring-[#2563EB]/20 resize-none"
            ></textarea>
          </div>

          <div class="flex flex-col gap-y-2.5">
            <label class="block text-sm font-semibold text-[#1F2937] tracking-[0.5%]">
              Местоположение
            </label>
            <input
              v-model="currentRequest.location"
              type="text"
              :readonly="!isEditing"
              :class="{ 'bg-gray-100': !isEditing }"
              class="w-full px-4 py-2.5 border border-[#E5E7EB] rounded-lg shadow-sm focus:border-[#2563EB] focus:ring-2 focus:ring-[#2563EB]/20"
            />
          </div>

          <div>
            <!-- Для активных заявок -->
            <template v-if="currentRequest.status === 'active' && !isEditing">
              <div class="pt-2.5 flex justify-between items-center">
                <button
                  @click="changeStatus(currentRequest, 'canceled')"
                  class="px-4 py-2 border border-solid border-[#2563EB] text-[#2563EB] rounded-lg text-[15px] font-semibold tracking-[0.5%] hover:bg-[#1D4ED8] hover:text-white"
                >
                  Отозвать
                </button>
                <button
                  @click="isEditing = true"
                  class="ml-2 px-4 py-2 bg-[#2563EB] text-white rounded-lg text-[15px] font-semibold tracking-[0.5%] hover:bg-[#1D4ED8]"
                >
                  Редактировать
                </button>
              </div>
            </template>

            <!-- Для заявок в работе -->
            <template v-else-if="currentRequest.status === 'in_progress' && !isEditing">
              <div class="pt-2.5 flex justify-between items-center">
                <button
                  @click="changeStatus(currentRequest, 'canceled')"
                  class="px-4 py-2 border border-solid border-[#2563EB] text-[#2563EB] rounded-lg text-[15px] font-semibold tracking-[0.5%] hover:bg-[#1D4ED8] hover:text-white"
                >
                  Отозвать
                </button>
                <button
                  @click="changeStatus(currentRequest, 'completed')"
                  class="px-4 py-2 bg-[#2563EB] text-white rounded-lg text-[15px] font-semibold tracking-[0.5%] hover:bg-[#1D4ED8]"
                >
                  Завершить
                </button>
              </div>
            </template>

            <!-- Для отозванных заявок -->
            <template v-else-if="currentRequest.status === 'canceled' && !isEditing">
              <button
                @click="changeStatus(currentRequest, 'active')"
                class="px-4 py-2 bg-[#2563EB] text-white rounded-lg text-[15px] font-semibold tracking-[0.5%] hover:bg-[#1D4ED8]"
              >
                Активировать
              </button>
            </template>

            <!-- Для редактирования -->
            <template v-if="isEditing">
              <div class="pt-2.5 flex justify-between items-center">
                <button
                  @click="isEditing = false"
                  class="px-4 py-2 border border-solid border-[#2563EB] text-[#2563EB] rounded-lg text-[15px] font-semibold tracking-[0.5%] hover:bg-[#1D4ED8] hover:text-white"
                >
                  Отменить
                </button>
                <button
                  type="submit"
                  class="px-4 py-2 bg-[#2563EB] text-white rounded-lg text-[15px] font-semibold tracking-[0.5%] hover:bg-[#1D4ED8]"
                >
                  Сохранить изменения
                </button>
              </div>
            </template>
          </div>
        </form>
      </div>
    </div>
  </section>
</template>
