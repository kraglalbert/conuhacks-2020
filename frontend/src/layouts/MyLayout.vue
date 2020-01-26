<template>
  <q-layout view="lHh Lpr lFf" id="container">
    <q-header>
      <q-toolbar class="bg-secondary">
        <q-toolbar-title>Welcome to your Wellness Hub</q-toolbar-title>
        <div>
          <q-btn
            flat
            round
            color="background"
            label="LOG OUT"
            @click="logout"
          />
        </div>
        <div>
          <q-btn flat round color="background" icon="home" to="/home" />
        </div>
      </q-toolbar>
    </q-header>

    <q-page-container>
      <router-view />
    </q-page-container>
  </q-layout>
</template>

<script>
import Activities from "../components/Activity.vue";
export default {
  name: "MyLayout",
  data() {
    return {
      leftDrawerOpen: false
    };
  },
  methods: {
    logout: function() {
      this.$store.dispatch("logout").then(this.$router.push({ path: "login" }));
    }
  }
};
</script>

<style lang="scss" scoped>
#container {
  background-color: $background;
  overflow: hidden !important;
}
</style>
