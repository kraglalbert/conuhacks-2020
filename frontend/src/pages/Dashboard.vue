<template>
  <q-page class="flex center row q-gutter-md">
    <div class="row q-gutter-md"> 
      <div class="col"> 
        <q-btn icon="rowing" label="Activities" stack color="dark" />
      </div>
      <div class="col"> 
        <q-btn icon="accessibility" label="Learning" stack class="col" color="dark" />
      </div>
    </div>
    <div class="row q-gutter-md">
      <div class="col"> 
        <q-btn icon="local_cafe" label="Coffee Date" stack class="col" color="dark" />
      </div>
      <div class="col"> 
        <q-btn icon="local_dining" label="Dining / Drinks" stack class="col" color="dark" />
      </div>
      <div class="col"> 
        <q-btn icon="calendar_today" label="Calendar" stack class="col" color="dark" />
      </div>
    </div>
  </q-page>
</template>

<script>

export default {
  name: 'Dashboard'
}
</script>
