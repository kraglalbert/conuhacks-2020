<template>
  <div
    id="container"
    class="row"
  >
  
    <q-btn
      class="row"
      style="min-width: 45px"
    >
      <center>
        <q-icon
          color="dark"
          :name="image"
          :size="'xl'"
        />
      </center>
    </q-btn>
    <div class="row q-pl-md q-pt-md">
      <div>{{ itemName }}</div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'HomeDeadlineItem',
  props: {
    itemName: String,
    image: String
  },
}
</script>
