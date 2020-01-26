<template>
  <q-page class="flex justify-center">
    <div class="row">
      <div class="col">
        <h4><strong>Activities</strong></h4>
      </div>
    </div>
    <div class="row">
      <div class="col"><EventList category="Activities" /></div>
    </div>
  </q-page>
</template>

<script>
import EventList from "../components/EventList.vue";

export default {
  name: "Activities",
  components: {
    EventList
  }
};
</script>
