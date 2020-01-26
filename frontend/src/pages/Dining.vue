<template>
  <q-page class="flex justify-center">
    <h4><strong>Dining</strong></h4>
    <EventList category="Food/Drink" />
  </q-page>
</template>

<script>
import EventList from "../components/EventList.vue";

export default {
  name: "Dining",
  components: {
    EventList
  }
};
</script>
