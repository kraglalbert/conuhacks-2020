<template>
  <div>
    <Event v-for="event in events" :key="event.id" :event="event" />
  </div>
</template>

<script>
import Event from "./Event.vue";

export default {
  name: "EventList",
  components: {
    Event
  },
  props: {
    category: String
  },
  data() {
    return {
      events: []
    };
  },
  created: function() {
    this.$axios
      .get("/events/filter", {
        params: {
          company_id: this.$store.state.currentUser.company_id,
          category: this.category
        }
      })
      .then(resp => {
        this.events = resp.data;
      });
  }
};
</script>
