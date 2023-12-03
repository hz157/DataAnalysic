<template>
    <div>
        <h2>Login</h2>
        <form @submit.prevent="login">
            <label for="username">Username:</label>
            <input type="text" id="username" v-model="username" required>
            <br>
            <label for="password">Password:</label>
            <input type="password" id="password" v-model="password" required>
            <br>
            <button type="submit">Login</button>
        </form>
    </div>
</template>

<script>
export default {}
</script>
<script>
export default {
    name: "Login",
    data() {
        return {
            username: '',
            password: '',
        };
    },
    methods: {
        login() {
            // 发送登录请求到后端
            const credentials = {
                username: this.username,
                password: this.password,
            };

            // 假设有一个名为login的API接口
            fetch('https://your-backend-api.com/login', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(credentials),
            })
                .then(response => response.json())
                .then(data => {
                    // 处理后端返回的数据，例如存储token等
                    console.log(data);
                })
                .catch(error => console.error('Error:', error));
        },
    },
};
</script>

<style scoped>

</style>