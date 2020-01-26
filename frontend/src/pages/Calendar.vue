<template>
  <div>
    <q-splitter
      v-model="splitterModel"
      style="height: 450px"
    >

      <template v-slot:before>
        <div class="q-pa-md">
          <q-date
            v-model="date"
            :events="event_dates"
            event-color="secondary"
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
          <q-tab-panel 
            v-for="e in event_dates"
            :key="e"
            :name="e"
          >
            <div class="text-h4 q-mb-md bg-secondary">Nice</div>
            <p>description</p>
          </q-tab-panel>

          <q-tab-panel name="2019/02/06">
            <div class="text-h4 q-mb">2019/02/06</div>
            <p class="bg-accent">Lorem ipsum dolor sit, amet consectetur adipisicing elit. Quis praesentium cumque magnam odio iure quidem, quod illum numquam possimus obcaecati commodi minima assumenda consectetur culpa fuga nulla ullam. In, libero.</p>
            <p>Lorem ipsum dolor sit, amet consectetur adipisicing elit. Quis praesentium cumque magnam odio iure quidem, quod illum numquam possimus obcaecati commodi minima assumenda consectetur culpa fuga nulla ullam. In, libero.</p>
            <p>Lorem ipsum dolor sit, amet consectetur adipisicing elit. Quis praesentium cumque magnam odio iure quidem, quod illum numquam possimus obcaecati commodi minima assumenda consectetur culpa fuga nulla ullam. In, libero.</p>
          </q-tab-panel>
        </q-tab-panels>
      </template>
    </q-splitter>
  </div>
</template>

<script>
export default {
  data () {
    return {
      splitterModel: 50,
      date: '',
      events: [],
      event_dates: [],

    }
  },
  created: function() {
        this.$axios.get('/events/filter', {
            params: {
                company_id: this.$store.state.currentUser.company_id
            }
        }).then(resp =>{
            this.events = resp.data
            this.events.forEach(e => {
                console.log(e.id);
                this.event_dates.push(e.date_time)
            });
        })
  }
}
</script>