<template>
  <div>
    <q-splitter v-model="splitterModel">
      <template v-slot:before>
        <div class="q-pa-md">
          <q-date
            v-if="events_type === 'All'"
            v-model="date"
            :events="event_dates"
            event-color="orange"
          />
          <q-date
            v-else
            v-model="date"
            :events="event_dates"
            event-color="orange"
          />
          <q-select
            borderless
            v-model="events_type"
            :options="options"
            label="Event Type"
            class="dropdown"
            @input="updateEvents"
          />
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
      event_dates: [],
      events_type: "All",
      options: ["All", "My RSVPs"]
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
  },
  methods: {
    updateEvents: function() {
      if (this.events_type === "All") {
        this.$axios
          .get("/events/filter", {
            params: {
              company_id: this.$store.state.currentUser.company_id
            }
          })
          .then(resp => {
            this.events = resp.data;
            this.event_dates = [];
            this.events.forEach(e => {
              this.event_dates.push(moment(e.date_time).format("YYYY/MM/DD"));
            });
          });
      } else {
        const user = this.$store.state.currentUser;
        this.$axios.get("/events/user/" + user.id + "/attending").then(resp => {
          this.events = resp.data;
          this.event_dates = [];
          this.events.forEach(e => {
            this.event_dates.push(moment(e.date_time).format("YYYY/MM/DD"));
          });
        });
      }
    }
  }
};
</script>

<style lang="scss" scoped>
.dropdown {
  width: 275px;
}
</style>
