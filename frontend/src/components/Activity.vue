<template>
    <div class="row">
        <q-btn
          class="row"
          style="min-width: 45px"
        >
          <center><bold>
              {{activityName}}
          </bold></center>
          <center>
              {{date}}
          </center>
        </q-btn>
    </div>
</template>

<script>
export default {
  name: 'HomeDeadlineItem',
  props: {
    activityName: String,
    date: String
  },
}
</script>