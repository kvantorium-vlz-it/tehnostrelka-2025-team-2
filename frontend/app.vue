<template>
  <div id="app">
    <!-- текст сайта + кнопки -->
    <div class="flex justify-center items-center h-screen bg-gray-100">
      <div class="bg-white p-8 rounded shadow-md w-60">  <!-- Заменили main-container на w-60 -->
        <h1 class="text-2xl font-semibold mb-6 text-center">Авторизация</h1>

        <form @submit.prevent="login">
          <div class="mb-4">
            <label for="name" class="block text-sm font-bold text-gray-700 mb-2">Имя:</label>
            <input
              type="name"
              id="name"
              v-model.trim="name"
              class="border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
              :class="{ 'border-red-500': errors.name }"
            />
            <p v-if="errors.name" class="text-red-500 text-xs italic">{{ errors.name }}</p>
          </div>

          <div class="mb-6">
            <label for="password" class="block text-sm font-bold text-gray-700 mb-2">Пароль:</label>
            <input
              type="password"
              id="password"
              v-model.trim="password"
              class="border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
              :class="{ 'border-red-500': errors.password }"
            />
            <p v-if="errors.password" class="text-red-500 text-xs italic">{{ errors.password }}</p>
          </div>

          <div class="flex items-center justify-between">
            <button
              type="submit"
              class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline"
              :disabled="loading"
            >
              <span v-if="!loading">Войти</span>
              <span v-else>Загрузка...</span>
            </button>
            <span v-if="loginError" class="text-red-500 text-xs italic">{{ loginError }}</span>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue';
import { useRouter } from 'vue-router';

const router = useRouter(); // Получаем экземпляр роутера

const name = ref('');
const password = ref('');
const loading = ref(false);
const loginError = ref(null);
const errors = reactive({
  name: null,
  password: null,
});

const validateForm = () => {
  errors.name = null;
  errors.password = null;
  let isValid = true;

  if (!name.value) {
    errors.name = 'Введите имя пользователя';
    isValid = false;
  }

  if (!password.value) {
    errors.password = 'Введите пароль';
    isValid = false;
  } else if (password.value.length < 6) {
      errors.password = 'Пароль должен содержать не менее 6 символов';
      isValid = false;
  }

  return isValid;
};

const login = async () => {
  if (!validateForm()) {
    return;
  }

  loading.value = true;
  loginError.value = null;

  // имитация запроса к api
  await new Promise(resolve => setTimeout(resolve, 1000));

  // проверка данных
  if (name.value === 'admin' && password.value === '123456') {
    console.log('Успешная авторизация');
    window.location.href = 'google.com'} 

  if (name.value === 'noway' && password.value === 'dexter') {
    console.log('Успешная авторизация');
    window.location.href = 'yandex.ru' }

  else {
    loginError.value = 'Неверное имя или пароль';
    console.error('Ошибка авторизации');
  }

  loading.value = false;
};
</script>
