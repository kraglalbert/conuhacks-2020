<template>
  <q-layout view="lHh Lpr lFf">
    <q-header>
      <q-toolbar>
        <q-toolbar-title>Welcome to your Wellness Hub</q-toolbar-title>

        <div>
          <q-btn icon="home" color="secondary" to="/"/>
        </div>
      </q-toolbar>
    </q-header>


    <q-page-container>
      <router-view />
    </q-page-container>
  </q-layout>
</template>

<script>
export default {
  name: "MyLayout",
  data() {
    return {
      leftDrawerOpen: false
    };
  }
};
</script>
