<script setup>
import { ref } from 'vue'

const name = ref('')
const password = ref('')
const valid = ref(false)
const message = ref('')

const nameRules = [
    value => {
        if (value) return true
        return 'Имя обязательно.'
    },
    value => {
        if (value?.length <= 20) return true
        return 'Имя не может состоять из 20+ символов'
    },
]

const passwordRules = [
    value => {
        if (value) return true
        return 'Пароль обязателен.'
    },
]

const login = () => {
    if (valid.value) {
        if (name.value === "admin" && password.value === "123456") {
            message.value = 'Успешная авторизация';
            window.location.href = 'https://google.com'
        } else {
            message.value = 'Неверное имя пользователя или пароль.';
        }
    }
}
</script>

<template>
    <div class="app-container">
        <v-form v-model="valid">
            <h1 class="text-h4 text-center font-weight-bold">Авторизация</h1>
            <v-text-field
                v-model="name"
                :counter="20"
                :rules="nameRules"
                label="Имя"
                required
                variant="outlined"
            ></v-text-field>
            <v-text-field
                v-model="password"
                :counter="10"
                :rules="passwordRules"
                label="Пароль"
                required
                variant="outlined"
                type="password"
            ></v-text-field>
            <v-btn @click="login" variant="outlined">
                Войти
            </v-btn>
            <div v-if="message" class="message">{{ message }}</div>
        </v-form>
    </div>
</template>

<style scoped>
.app-container {
  background-color: rgb(61, 61, 61); /* Черный фон для контейнера */
  min-height: 100vh; /* Минимальная высота 100% от высоты видимой области */
  display: flex;
  align-items: center; /* Вертикальное центрирование */
  justify-content: center; /* Горизонтальное центрирование */
  color: white; /* Цвет текста */
  width: 90%; /* Ширина контейнера (можно настроить по своему вкусу) */
  max-width: 1024px; /* Максимальная ширина, чтобы форма не становилась слишком широкой */
  margin: 0 auto; /* Центрирование контейнера на странице */
  padding: 20px; /* Отступы внутри контейнера */
}

.message {
    color: red;
    text-align: center;
    margin-top: 10px;
}
</style>