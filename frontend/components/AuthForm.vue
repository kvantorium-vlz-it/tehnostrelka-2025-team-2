<script setup>
const name = ref('')
const password = ref('')
const valid = ref(false)

const nameRules = [
    value => {
        if (value) return true

        return 'Имя обязательно.'
    },
    value => {
        if (value?.length <= 20) return true

        return 'Имя должно не может состоять из 20+ символов'
    },
]

const passwordRules = [
    value => {
        if (value) return true

        return 'Пароль обязателен.'
    },
]
</script>

<template>
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
        ></v-text-field>
        <v-btn variant="outlined">
            Войти
        </v-btn>
    </v-form>
</template>
