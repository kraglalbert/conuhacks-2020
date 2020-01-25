<template>
  <q-page class="flex center row q-gutter-md">
    <div class="row q-gutter-md"> 
      <div class="col"> 
        <q-btn icon="rowing" label="Activities" stack color="dark" to="/activities"/>
      </div>
      <div class="col"> 
        <q-btn icon="accessibility" label="Learning" stack class="col" color="dark" to="/learning"/>
      </div>
    </div>
    <div class="row q-gutter-md">
      <div class="col"> 
        <q-btn icon="local_cafe" label="Coffee Date" stack class="col" color="dark" to="/coffee"/>
      </div>
      <div class="col"> 
        <q-btn icon="local_dining" label="Dining / Drinks" stack class="col" color="dark" to="/dining"/>
      </div>
      <div class="col"> 
        <q-btn icon="calendar_today" label="Calendar" stack class="col" color="dark" to="/calendar"/>
      </div>
    </div>
  </q-page>
</template>

<script>

export default {
  name: 'Dashboard'
}
</script>
