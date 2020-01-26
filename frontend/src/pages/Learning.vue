<template>
  <q-page id="container">
    <div>
      <div class="row">
        <div class="col">
          <h4><strong>Learning</strong></h4>
        </div>
      </div>
      <div class="row">
        <div class="col"><EventList category="Learning" /></div>
      </div>
    </div>
  </q-page>
</template>

<script>
import EventList from "../components/EventList.vue";

export default {
  name: "Learning",
  components: {
    EventList
  }
};
</script>

<style lang="scss" scoped>
#container {
  width: 85%;
  margin-left: 7.5%;
  margin-right: 7.5%;
}
</style>
