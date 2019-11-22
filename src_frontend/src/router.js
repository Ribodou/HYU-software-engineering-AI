import Vue from 'vue'
import Router from 'vue-router'

const Home = () => import ('@/components/Home.vue')
const Game = () => import ('@/components/Game.vue')

Vue.use(Router)


export default new Router({
    mode: 'history',
    base: '/',
    routes: [
        {
            path: '/',
            redirect: '/home'
        },
        {
            name: "Home",
            path: '/home',
            component: Home
        },
        {
            name: 'Game',
            path: '/game/:id',
            component: Game
        },
        // Not found route
        {
            path: '*',
            redirect: '/'
        }
    ]
})