<template>
    <header id="header">

        <div id="logo-group">
            <span id="logo"><img src="../assets/logo.png" alt="youmuto"> </span>
        </div>

    </header>
</template>

<script>
    export default {
        data() {
            return {

            }
        },

        created() {
        },

        methods: {
            logout() {
                window.localStorage.removeItem('userhashid');
                window.location = '/login';
            }
        }
    }
</script>
