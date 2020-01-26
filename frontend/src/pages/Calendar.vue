<template>
  <div>
    <q-splitter v-model="splitterModel">
      <template v-slot:before>
        <div class="q-pa-md">
          <q-date v-model="date" :events="event_dates" event-color="orange" />
        </div>
      </template>

      <template v-slot:after>
        <q-tab-panels
          v-model="date"
          animated
          transition-prev="jump-up"
          transition-next="jump-up"
        >
          <q-tab-panel class="bg-accent" :name="date">
            <CalendarItemList :events="events" :date="date" />
          </q-tab-panel>
        </q-tab-panels>
      </template>
    </q-splitter>
  </div>
</template>

<script>
import moment from "moment";
import CalendarItemList from "../components/CalendarItemList.vue";

export default {
  components: {
    CalendarItemList
  },
  data() {
    return {
      splitterModel: 50,
      date: moment(new Date()).format("YYYY/MM/DD"),
      events: [],
      event_dates: []
    };
  },
  created: function() {
    this.$axios
      .get("/events/filter", {
        params: {
          company_id: this.$store.state.currentUser.company_id
        }
      })
      .then(resp => {
        this.events = resp.data;
        this.events.forEach(e => {
          this.event_dates.push(moment(e.date_time).format("YYYY/MM/DD"));
        });
      });
  }
};
</script>
