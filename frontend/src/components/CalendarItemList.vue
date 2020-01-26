<template>
    <div>
        <CalendarItem v-for="e in filtered_events" :key="e.id" :event="e" />
    </div>
</template>

<script>
import moment from "moment";
import CalendarItem from "./CalendarItem.vue"

export default {
  name: 'CalendarItemList',
  components: {
    CalendarItem
  },
  props: {
    events: Array,
    date: String
  },
  data() {
      return {
          filtered_events: this.events.filter(e => moment(e.date_time).format("YYYY/MM/DD") === this.date)
      }
  }
}
</script>