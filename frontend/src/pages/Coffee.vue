<template>
  <q-page class="flex justify-center">
    <h4><strong>Coffee Dates</strong></h4>
    <EventList category="Coffee Dates" />
  </q-page>
</template>

<script>
import EventList from "../components/EventList.vue";

export default {
  name: "Coffee",
  components: {
    EventList
  }
};
</script>
