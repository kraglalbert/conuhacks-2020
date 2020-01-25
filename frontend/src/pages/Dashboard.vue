<template>
  <q-page class="flex flex-left q-pl-xl row
  ">
    <dashitem itemName="Activities" image="rowing"/>
    <dashitem itemName="Learning" image="accessibility"/>
    <dashitem itemName="Coffee Date" image="local_cafe"/>
    <dashitem itemName="Dining / Drinks" image="local_dining"/>
    <dashitem itemName="Calendar" image="calendar_today"/>
  </q-page>
</template>

<script>
import dashitem from '../components/DashItem.vue'

export default {
  name: 'Dashboard',
  components: {
      dashitem
  }
}
</script>
