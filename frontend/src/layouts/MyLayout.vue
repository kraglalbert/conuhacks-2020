<template>
  <q-layout view="lHh Lpr lFf">
    <q-header>
      <q-toolbar class="bg-secondary">
        <q-toolbar-title>Welcome to your Wellness Hub</q-toolbar-title>
        <div>
          <q-btn
            icon="home"
            color="secondary"
            to="/home"
          />
        </div>
      </q-toolbar>
    </q-header>

    <q-page-container id="container">
      <router-view />
    </q-page-container>
  </q-layout>
</template>

<script>
export default {
  name: "MyLayout",
  data () {
    return {
      leftDrawerOpen: false
    };
  }
};
</script>

<style lang="scss" scoped>
#container {
  background-color: $background;
  overflow: hidden !important;
}
</style>
