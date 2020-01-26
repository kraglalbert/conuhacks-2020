<template>
  <q-page class="flex flex-center">
    <div class="q-pa-md">
      <div class="row q-col-gutter-md justify-center">
        <div class="col">
          <q-btn
            icon="rowing"
            label="Activities"
            class="dashboard-button"
            stack
            color="primary"
            to="/activities"
          />
        </div>
        <div class="col">
          <q-btn
            icon="accessibility"
            label="Learning"
            class="dashboard-button"
            stack
            color="primary"
            to="/learning"
          />
        </div>
        <div class="col">
          <q-btn
            icon="local_cafe"
            label="Coffee Date"
            class="dashboard-button"
            stack
            color="primary"
            to="/coffee"
          />
        </div>
        <div class="col">
          <q-btn
            icon="local_dining"
            label="Dining / Drinks"
            stack
            class="dashboard-button"
            color="primary"
            to="/dining"
          />
        </div>
        <div class="col">
          <q-btn
            icon="calendar_today"
            label="Calendar"
            stack
            class="dashboard-button"
            color="primary"
            to="/calendar"
          />
        </div>
      </div>
      <div class="row justify-center full-height full-width text-center">
        <div class="col">
          <q-btn
            label="Host Event"
            stack
            class="host-button"
            color="primary"
            @click="showHostEventPopUp = true"
          />
        </div>
      </div>
    </div>
    <q-dialog v-model="showHostEventPopUp">
      <HostEventPopUp @dialog-closed="showHostEventPopUp = false" />
    </q-dialog>
  </q-page>
</template>

<script>
import HostEventPopUp from "../components/HostEventPopUp.vue";

export default {
  name: "Dashboard",
  components: {
    HostEventPopUp
  },
  data() {
    return {
      showHostEventPopUp: false
    };
  }
};
</script>

<style lang="scss" scoped>
.dashboard-button {
  width: 180px;
  height: 120px;
}
.host-button {
  margin-top: 5%;
}
</style>
