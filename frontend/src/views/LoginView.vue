<template>
  <!--<div>
    <login-form />
  </div>-->
  <div>
    <button @click="login">Log in</button>
  </div>
</template>

<script>
// import LoginForm from "@/components/LoginForm.vue";
export default {
  methods: {
    login() {
      this.$auth0.loginWithRedirect();
    },
  },
};
</script>
