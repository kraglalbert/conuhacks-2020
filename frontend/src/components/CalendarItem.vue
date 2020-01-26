<template>
    <div>
        <div class="text-h4 q-mb " >{{event.name}}</div>
        <p>{{event.date_time}}</p>
        <q-badge class="primary">{{event.category}}</q-badge>
            <p>{{event.description}}</p>
        <q-btn :disable='btnEnable' class="q-mb-sm" label="RSVP" stack color="primary" @click="addUserToEvent" />
        <q-separator />
    </div>
</template>

<script>
import moment from "moment";

export default {
  name: 'CalendarItemList',
  props: {
    event: Object,
  },
  data() {
    return {
      btnEnable: false
    };
  },
  computed: {
    isEnabled: function(){
      return this.btnEnable;
    }
  },
  created: function() {
    var a;
    let user = this.$store.state.currentUser;

    this.event.attendees.forEach(a => {
       if(a.id === user.id){
        console.log('Hello World')
        this.btnEnable = true;
      }
    })
  },
    methods: {
      addUserToEvent: function() {
        let user = this.$store.state.currentUser;

        const data = {
          attendee_email: user.email
        };
        this.$axios
          .put("/events/" + this.event.id + "/add-attendee", data, {
            headers: {
              Authorization: this.$store.state.token
            }
          })
          .then(_resp => {
            this.$q.notify({
              color: "green-4",
              position: "top",
              textColor: "white",
              icon: "cloud_done",
              message: "RSVP'd Successfully"
            });
            // let parent know to close the dialog
            this.$emit("dialog-closed");
          })
          .catch(_err => {
            this.$q.notify({
              color: "red-4",
              position: "top",
              textColor: "white",
              icon: "error",
              message: "Something went wrong, please try again"
            });
          });
      }
  }
}
</script>