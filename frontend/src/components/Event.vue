<template>
  <q-card>
    <q-card-section>
      <h5>
        <strong>{{ event.name }}</strong>
      </h5>
      <p>
        <i> {{ event.description }}</i>
      </p>
      <p>{{ event.date_time }}</p>
      <q-btn label="RSVP" stack color="primary" @click="addUserToEvent" />
    </q-card-section>
  </q-card>
</template>

<script>
export default {
  props: {
    event: Object
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
};
</script>
