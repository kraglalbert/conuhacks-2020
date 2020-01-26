<template>
  <q-card class="event-popup">
    <q-card-section class="row items-center">
      <div class="text-h6">Add New Event</div>
      <q-space />
      <q-btn icon="close" flat round dense v-close-popup />
    </q-card-section>

    <q-card-section>
      <q-form @submit="createEvent" class="q-gutter-sm">
        <q-input
          filled
          v-model="eventTitle"
          label="Event Title"
          lazy-rules
          :rules="[
            val => (val && val.length > 0) || 'Please enter an event title'
          ]"
        />

        <q-input
          v-model="description"
          filled
          type="textarea"
          label="Event Description"
          lazy-rules
          :rules="[
            val => (val && val.length > 0) || 'Please enter a description',
            val =>
              (val && val.length < 64) ||
              'Descriptions must be less than 64 characters'
          ]"
        />

        <q-select
          v-model="eventCategory"
          filled
          :options="categories"
          label="Event Category"
          lazy-rules
          :rules="[
            val => (val && val.length > 0) || 'Please enter an event category'
          ]"
        />

        <q-input
          filled
          v-model="eventLocation"
          label="Event Location"
          lazy-rules
          :rules="[
            val => (val && val.length > 0) || 'Please enter an event location'
          ]"
        />

        <q-input
          filled
          v-model="eventTime"
          label="Time"
          mask="time"
          :rules="['time']"
        >
          <template v-slot:append>
            <q-icon name="access_time" class="cursor-pointer">
              <q-popup-proxy transition-show="scale" transition-hide="scale">
                <q-time v-model="eventTime" />
              </q-popup-proxy>
            </q-icon>
          </template>
        </q-input>

        <q-input
          filled
          v-model="eventDate"
          label="Date"
          mask="date"
          :rules="['date']"
        >
          <template v-slot:append>
            <q-icon name="event" class="cursor-pointer">
              <q-popup-proxy
                ref="qDateProxy"
                transition-show="scale"
                transition-hide="scale"
              >
                <q-date
                  v-model="eventDate"
                  @input="() => $refs.qDateProxy.hide()"
                />
              </q-popup-proxy>
            </q-icon>
          </template>
        </q-input>

        <q-btn color="primary" type="submit" label="Add" />
      </q-form>
    </q-card-section>
  </q-card>
</template>

<script>
import moment from "moment";

export default {
  name: "HostEventPopup",
  data() {
    return {
      eventDate: moment(new Date()).format("YYYY/MM/DD"),
      description: "",
      eventTitle: "",
      eventCategory: "",
      eventLocation: "",
      eventTime: "",
      eventDate: "",
      categories: []
    };
  },
  created: function() {
    this.$axios.get("/events/categories").then(resp => {
      this.categories = resp.data;
    });
  },
  methods: {
    createEvent: function() {
      const user = this.$store.state.currentUser;
      const date_time = moment(
        new Date(this.eventDate + " " + this.eventTime)
      ).format("DD-MM-YYYY h:mma");
      console.log(this.eventTime);
      console.log(date_time);

      const data = {
        event_name: this.eventTitle,
        description: this.description,
        location: this.eventLocation,
        category: this.eventCategory,
        date_time: date_time,
        host_email: this.$store.state.currentUser.email
      };
      this.$axios
        .post("/events", data, {
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
            message: "Event Created Successfully"
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

<style lang="scss" scoped>
.event-popup {
  min-width: 500px;
}
</style>
