<template>
    <div>
        <h1>Connect Four</h1>
        <h3>Your game ID: {{ $route.params.id }}</h3>
        <small>Save the Link or ID to continue another time! <a :href="currentLocation">{{ currentLocation }}</a></small>
        <br>
        <br>
        <game-container></game-container>
    </div>
</template>

<script>
    import GameContainer from '@/components/GameContainer.vue'

    export default {
        name: 'Game',
        components: {
            GameContainer
        },
        computed: {
            currentLocation(){
                return window.location.href
            }
        }
    }
</script>
