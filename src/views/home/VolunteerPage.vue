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
    status: 'new',
    volunteerId: null,
  },
  {
    id: 2,
    title: 'Требуются лекарства',
    type: 'medicine',
    description: 'Нужны лекарства для пожилого человека',
    location: 'Санкт-Петербург, ул. Пушкина 5',
    createdAt: new Date(Date.now() - 86400000).toLocaleString(),
    status: 'in_progress',
    volunteerId: 1,
  },
  {
    id: 3,
    title: 'Продукты первой необходимости',
    type: 'food',
    description: 'Нужны продукты для семьи из 4 человек',
    location: 'Казань, ул. Гоголя 15',
    createdAt: new Date(Date.now() - 172800000).toLocaleString(),
    status: 'new',
    volunteerId: 1,
  },
  {
    id: 4,
    title: 'Помощь с ремонтом',
    type: 'other',
    description: 'Требуется помощь с ремонтом квартиры',
    location: 'Новосибирск, ул. Советская 20',
    createdAt: new Date(Date.now() - 259200000).toLocaleString(),
    status: 'new',
    volunteerId: null,
  },
  {
    id: 5,
    title: 'Транспорт для доставки',
    type: 'transport',
    description: 'Нужен транспорт для доставки гуманитарной помощи',
    location: 'Екатеринбург, ул. Мира 8',
    createdAt: new Date(Date.now() - 345600000).toLocaleString(),
    status: 'in_progress',
    volunteerId: 2,
  },
  {
    id: 6,
    title: 'Медицинская консультация',
    type: 'medicine',
    description: 'Требуется консультация врача',
    location: 'Ростов-на-Дону, ул. Красноармейская 3',
    createdAt: new Date(Date.now() - 432000000).toLocaleString(),
    status: 'completed',
    volunteerId: 1,
  },
  {
    id: 7,
    title: 'Медицинская консультация',
    type: 'medicine',
    description: 'Требуется консультация врача',
    location: 'Ростов-на-Дону, ул. Красноармейская 3',
    createdAt: new Date(Date.now() - 432000000).toLocaleString(),
    status: 'new',
    volunteerId: 1,
  },
  {
    id: 8,
    title: 'Медицинская консультация',
    type: 'medicine',
    description: 'Требуется консультация врача',
    location: 'Ростов-на-Дону, ул. Красноармейская 3',
    createdAt: new Date(Date.now() - 432000000).toLocaleString(),
    status: 'completed',
    volunteerId: 1,
  },
  {
    id: 9,
    title: 'Медицинская консультация',
    type: 'medicine',
    description: 'Требуется консультация врача',
    location: 'Ростов-на-Дону, ул. Красноармейская 3',
    createdAt: new Date(Date.now() - 432000000).toLocaleString(),
    status: 'new',
    volunteerId: 1,
  },
  {
    id: 10,
    title: 'Медицинская консультация',
    type: 'medicine',
    description: 'Требуется консультация врача',
    location: 'Ростов-на-Дону, ул. Красноармейская 3',
    createdAt: new Date(Date.now() - 432000000).toLocaleString(),
    status: 'completed',
    volunteerId: 1,
  },
])

// Состояние для отображения всех заявок
const showAllNew = ref(false)
const showAllInProgress = ref(false)
const showAllCompleted = ref(false)

const selectedType = ref('')
const selectedLocation = ref('')

// Отображение только 4 последних заявок
const displayedNewRequests = computed(() => {
  return showAllNew.value ? [...newRequests.value] : newRequests.value.slice(0, 4)
})

const displayedInProgressRequests = computed(() => {
  return showAllInProgress.value
    ? [...inProgressRequests.value]
    : inProgressRequests.value.slice(0, 4)
})

const displayedCompletedRequests = computed(() => {
  return showAllCompleted.value ? [...completedRequests.value] : completedRequests.value.slice(0, 4)
})

// Текущий волонтер
const currentVolunteer = ref({
  id: 1,
  name: 'Иван Иванов',
  tel: '+79123456789',
})

// Состояние модальных окон
const showViewModal = ref(false)
const currentRequest = ref(null)

// Цвета и тексты для статусов
const statusConfig = {
  new: {
    text: 'Новая',
    color: '#FEF9C3',
    textColor: '#854D0E',
  },
  in_progress: {
    text: 'В работе',
    color: '#DBEAFE',
    textColor: '#1E40AF',
  },
  completed: {
    text: 'Завершена',
    color: '#DBFEDB',
    textColor: '#1EAF53',
  },
}
// Фильтрация заявок по статусам
const newRequests = computed(() => {
  return requests.value
    .filter((request) => request.status === 'new')
    .filter(
      (request) =>
        (!selectedType.value || request.type === selectedType.value) &&
        (!selectedLocation.value || request.location.includes(selectedLocation.value)),
    )
    .sort((a, b) => new Date(b.createdAt) - new Date(a.createdAt))
})

const inProgressRequests = computed(() => {
  return requests.value
    .filter(
      (request) =>
        request.status === 'in_progress' && request.volunteerId === currentVolunteer.value.id,
    )
    .filter(
      (request) =>
        (!selectedType.value || request.type === selectedType.value) &&
        (!selectedLocation.value || request.location.includes(selectedLocation.value)),
    )
    .sort((a, b) => new Date(b.createdAt) - new Date(a.createdAt))
})

const completedRequests = computed(() => {
  return requests.value
    .filter(
      (request) =>
        request.status === 'completed' && request.volunteerId === currentVolunteer.value.id,
    )
    .filter(
      (request) =>
        (!selectedType.value || request.type === selectedType.value) &&
        (!selectedLocation.value || request.location.includes(selectedLocation.value)),
    )
    .sort((a, b) => new Date(b.createdAt) - new Date(a.createdAt))
})

// Открытие заявки для просмотра
const openRequest = (request) => {
  currentRequest.value = { ...request }
  showViewModal.value = true
}

// Волонтер откликается на заявку
const respondToRequest = () => {
  const index = requests.value.findIndex((r) => r.id === currentRequest.value.id)
  if (index !== -1) {
    requests.value[index].status = 'in_progress'
    requests.value[index].volunteerId = currentVolunteer.value.id
  }
  showViewModal.value = false
}

// Завершение заявки
const completeRequest = () => {
  const index = requests.value.findIndex((r) => r.id === currentRequest.value.id)
  if (index !== -1) {
    requests.value[index].status = 'completed'
  }
  showViewModal.value = false
}

// Обновление заявки
const updateRequest = () => {
  const index = requests.value.findIndex((r) => r.id === currentRequest.value.id)
  if (index !== -1) {
    requests.value[index] = { ...currentRequest.value }
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

const openYandexMap = () => {
  if (!currentRequest.value?.location) return

  // Кодируем адрес для URL
  const encodedAddress = encodeURIComponent(currentRequest.value.location)

  // Формируем URL для Яндекс.Карт
  const yandexMapsUrl = `https://yandex.ru/maps/?text=${encodedAddress}`

  // Открываем в новом окне
  window.open(yandexMapsUrl, '_blank')
}

const agreeToShareContacts = ref(false)
const showModal = ref(false)
</script>

<template>
  <section class="px-10 pt-25">
    <div class="flex flex-col xs:flex-row justify-between xs:items-center gap-2.5 pb-5">
      <h3 class="font-semibold tracking-[0.5%] text-[#1F2937] text-[32px] xs:pb-5">
        Заявки от ветеранов
      </h3>
      <button
        type="button"
        class="py-2.5 px-4 text-white bg-[#2563EB] rounded-lg text-[15px] font-semibold tracking-[0.5%]"
        @click="showModal = true"
      >
        Карта
      </button>
    </div>

    <div
      v-if="showModal"
      class="fixed inset-0 z-50 overflow-y-auto bg-black/50 flex items-center justify-center"
    >
      <div class="bg-white rounded-[20px] p-10 shadow-lg max-w-lg w-full mx-4 relative">
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
        <p class="text-center text-lg font-bold text-[#1F2937] tracking-[0.5%]">
          Интерактиванная карта
        </p>
      </div>
    </div>

    <!-- Информация о волонтере -->
    <div class="p-4 bg-blue-50 rounded-lg">
      <h4 class="text-xl font-semibold">{{ currentVolunteer.name }}</h4>
      <p class="text-xs text-gray-600 mt-1">ID: {{ currentVolunteer.id }}</p>
      <a href="tel:+79123456789">{{ currentVolunteer.tel }}</a>
    </div>

    <!-- Replace your current filter controls with this -->
    <div class="pt-5 flex gap-7.5">
      <div class="flex flex-col gap-y-2.5 w-80">
        <label class="block text-xs font-semibold text-[#1F2937] tracking-[0.5%]">
          Тип помощи
        </label>
        <select
          v-model="selectedType"
          class="w-full px-4 py-2.5 border border-[#E5E7EB] rounded-lg shadow-xs focus:border-[#2563EB] focus:ring-2 focus:ring-[#2563EB]/20"
        >
          <option value="">Все</option>
          <option value="transport">Транспорт</option>
          <option value="food">Продукты</option>
          <option value="medicine">Лекарства</option>
          <option value="other">Другое</option>
        </select>
      </div>

      <div class="flex flex-col gap-y-2.5 w-80">
        <label class="block text-xs font-semibold text-[#1F2937] tracking-[0.5%]">
          Местоположение
        </label>
        <input
          v-model="selectedLocation"
          list="locations"
          placeholder="Введите город"
          class="w-full px-4 py-2.5 border border-[#E5E7EB] rounded-lg shadow-xs focus:border-[#2563EB] focus:ring-2 focus:ring-[#2563EB]/20"
        />
        <datalist id="locations" class="w-full bg-green">
          <option value="Москва" class="w-full"></option>
          <option value="Санкт-Петербург" class="w-full"></option>
          <option value="Казань" class="w-full"></option>
          <option value="Новосибирск" class="w-full"></option>
          <option value="Екатеринбург" class="w-full"></option>
          <option value="Ростов-на-Дону" class="w-full"></option>
        </datalist>
      </div>
    </div>

    <!-- Секция "Новые заявки" -->
    <div class="mb-12">
      <h4 class="text-xl font-semibold pb-2.5 pt-5">Новые заявки</h4>
      <div class="flex gap-5 flex-wrap pb-5">
        <div
          v-for="request in displayedNewRequests"
          :key="request.id"
          class="w-full md:w-[calc(50%-10px)] p-5 bg-white rounded-lg flex flex-col gap-y-4 shadow-xs border border-[#E5E7EB] cursor-pointer hover:shadow-md transition-shadow"
          @click="openRequest(request)"
        >
          <div class="flex flex-col xs:flex-row justify-between items-start gap-2.5">
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
      <div class="flex justify-end pb-2.5" v-if="newRequests.length >= 4">
        <button
          @click="showAllNew = !showAllNew"
          class="px-4 py-2 text-[#2563EB] border border-[#2563EB] rounded-lg hover:bg-[#2563EB] hover:text-white transition-colors w-full xs:w-fit"
        >
          {{ showAllNew ? 'Скрыть' : 'Все' }}
        </button>
      </div>
      <div v-if="newRequests.length === 0" class="text-center py-4 text-gray-500">
        Нет новых заявок
      </div>
    </div>

    <!-- Секция "Заявки в работе" -->
    <div class="mb-12">
      <h4 class="text-xl font-semibold pb-2.5">Заявки в работе</h4>
      <div class="flex gap-5 flex-wrap pb-5">
        <div
          v-for="request in displayedInProgressRequests"
          :key="request.id"
          class="w-full md:w-[calc(50%-10px)] p-5 bg-white rounded-lg flex flex-col gap-y-4 shadow-xs border border-[#E5E7EB] cursor-pointer hover:shadow-md transition-shadow"
          @click="openRequest(request)"
        >
          <div class="flex flex-col xs:flex-row justify-between items-start gap-2.5">
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
      <div class="flex justify-end pb-5" v-if="inProgressRequests.length >= 4">
        <button
          @click="showAllInProgress = !showAllInProgress"
          class="px-4 py-2 text-[#2563EB] border border-[#2563EB] rounded-lg hover:bg-[#2563EB] hover:text-white transition-colors w-full xs:w-fit"
        >
          {{ showAllInProgress ? 'Скрыть' : 'Все' }}
        </button>
      </div>
      <div v-if="inProgressRequests.length === 0" class="text-center py-4 text-gray-500">
        Нет заявок в работе
      </div>
    </div>

    <!-- Секция "Завершенные заявки" -->
    <div class="mb-12">
      <h4 class="text-xl font-semibold pb-2.5">Завершенные заявки</h4>
      <div class="flex gap-5 flex-wrap pb-5">
        <div
          v-for="request in displayedCompletedRequests"
          :key="request.id"
          class="w-full md:w-[calc(50%-10px)] p-5 bg-white rounded-lg flex flex-col gap-y-4 shadow-xs border border-[#E5E7EB] cursor-pointer hover:shadow-md transition-shadow"
          @click="openRequest(request)"
        >
          <div class="flex flex-col xs:flex-row justify-between items-start gap-2.5">
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
      <!-- Кнопка "Все" для завершенных заявок -->
      <div class="flex justify-end pb-5" v-if="completedRequests.length >= 4">
        <button
          @click="showAllCompleted = !showAllCompleted"
          class="px-4 py-2 text-[#2563EB] border border-[#2563EB] rounded-lg hover:bg-[#2563EB] hover:text-white transition-colors w-full xs:w-fit"
        >
          {{ showAllCompleted ? 'Скрыть' : 'Все' }}
        </button>
      </div>
      <div v-if="completedRequests.length === 0" class="text-center py-4 text-gray-500">
        Нет завершенных заявок
      </div>
    </div>

    <!-- Модальное окно просмотра заявки -->
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
          Заявка
        </h2>

        <form @submit.prevent="updateRequest" class="flex flex-col gap-y-2.5">
          <div class="flex flex-col gap-y-2.5">
            <label class="block text-xs font-semibold text-[#1F2937] tracking-[0.5%]">
              Тема заявки
            </label>
            <input
              v-model="currentRequest.title"
              type="text"
              required
              class="w-full px-4 py-2.5 border border-[#E5E7EB] bg-gray-100 rounded-lg shadow-xs focus:border-[#2563EB] focus:ring-2 focus:ring-[#2563EB]/20"
            />
          </div>

          <div class="flex flex-col gap-y-2.5">
            <label class="block text-xs font-semibold text-[#1F2937] tracking-[0.5%]">
              Тип помощи
            </label>
            <select
              v-model="currentRequest.type"
              required
              class="w-full px-4 py-2.5 border border-[#E5E7EB] bg-gray-100 rounded-lg shadow-xs focus:border-[#2563EB] focus:ring-2 focus:ring-[#2563EB]/20"
            >
              <option value="transport">Транспорт</option>
              <option value="food">Продукты</option>
              <option value="medicine">Лекарства</option>
              <option value="other">Другое</option>
            </select>
          </div>

          <div class="flex flex-col gap-y-2.5">
            <label class="block text-xs font-semibold text-[#1F2937] tracking-[0.5%]">
              Описание
            </label>
            <textarea
              v-model="currentRequest.description"
              rows="5"
              class="w-full px-4 py-2.5 border border-[#E5E7EB] bg-gray-100 rounded-lg shadow-xs focus:border-[#2563EB] focus:ring-2 focus:ring-[#2563EB]/20 resize-none"
            ></textarea>
          </div>

          <div class="flex flex-col gap-y-2.5">
            <label class="block text-xs font-semibold text-[#1F2937] tracking-[0.5%]">
              Местоположение
            </label>
            <input
              v-model="currentRequest.location"
              type="text"
              class="w-full px-4 py-2.5 border border-[#E5E7EB] bg-gray-100 rounded-lg shadow-xs focus:border-[#2563EB] focus:ring-2 focus:ring-[#2563EB]/20"
            />
          </div>

          <a
            @click.prevent="openYandexMap"
            class="block text-[#2563EB] text-xs font-medium tracking-[0.5%] cursor-pointer hover:underline"
          >
            Посмотреть на карте
          </a>

          <div class="flex items-center gap-x-2 pt-2.5">
            <input
              type="checkbox"
              id="userType"
              v-model="agreeToShareContacts"
              class="w-4 h-4 text-[#2563EB] rounded border-[#E5E7EB] focus:ring-[#2563EB]"
            />
            <label for="userType" class="text-base font-medium tracking-[0.5%] text-[#1F2937]">
              Согласен поделиться своими контактными данными с заявителем
            </label>
          </div>

          <div>
            <!-- Для заявок в работе -->
            <template v-if="currentRequest.status === 'in_progress'">
              <div class="pt-2.5 flex justify-center items-center">
                <button
                  @click="changeStatus(currentRequest, 'completed')"
                  class="px-4 py-2 bg-[#2563EB] text-white rounded-lg text-[15px] font-semibold tracking-[0.5%] hover:bg-[#1D4ED8]"
                >
                  Завершить
                </button>
              </div>
            </template>

            <!-- Для новых заявок -->
            <template v-else-if="currentRequest.status === 'new'">
              <div class="pt-2.5 flex justify-center items-center">
                <button
                  @click="changeStatus(currentRequest, 'in_progress')"
                  :disabled="!agreeToShareContacts"
                  :class="{
                    'bg-[#2563EB] hover:bg-[#1D4ED8]': agreeToShareContacts,
                    'bg-gray-400 cursor-not-allowed': !agreeToShareContacts,
                  }"
                  class="px-4 py-2 bg-[#2563EB] text-white rounded-lg text-[15px] font-semibold tracking-[0.5%] hover:bg-[#1D4ED8]"
                >
                  Откликнуться
                </button>
              </div>
            </template>
          </div>
        </form>
      </div>
    </div>
  </section>
</template>
