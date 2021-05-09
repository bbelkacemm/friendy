import Vue from 'vue'
import VueRouter from 'vue-router'
import App from '@/App'
import Login from '@/views/Login'
import Signup from '@/views/Signup'
import Home from '@/views/Home'
import Users from '@/views/Users'
import Roles from '@/views/Roles'
import Contexts from '@/views/Contexts'
import Dashboard from '@/views/Dashboard'
import Contributions from '@/views/Contributions'

Vue.use(VueRouter)

const routes = [
    {
        path: '/',
        component: App,
        redirect: 'home',
    },
    {
        path: '/login',
        name: 'login',
        component: Login,
    },
    {
        path: '/signup',
        name: 'signup',
        component: Signup,
    },
    {
        path: '/home',
        name: 'home',
        component: Home,
    },
    {
        path: '/dashboard',
        name: 'dashboard',
        component: Dashboard,
    },
    {
        path: '/users',
        name: 'users',
        component: Users,
    },
    {
        path: '/roles',
        name: 'roles',
        component: Roles,
    },
    {
        path: '/contributions',
        name: 'contributions',
        component: Contributions,
    },
    {
        path: '/contexts',
        name: 'contexts',
        component: Contexts,
    },
]

const router = new VueRouter({
    mode: 'history',
    base: process.env.BASE_URL,
    routes,
})

export default router