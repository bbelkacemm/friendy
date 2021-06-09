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
import NotFound from '@/views/NotFound'
import Models from '@/views/Models'
import store from '@/store'
import { ADMINISTRATOR, CLIENT, CONTRIBUTOR, GUEST, MODERATOR } from '@/constants'
import NotAuthorized from '@/views/NotAuthorized'

Vue.use(VueRouter)

const routes = [
    {
        path: '/',
        component: App,
        redirect: 'home',
        allowed: [ADMINISTRATOR, MODERATOR, CONTRIBUTOR, CLIENT, GUEST],
    },
    {
        path: '/login',
        name: 'login',
        component: Login,
        allowed: [ADMINISTRATOR, MODERATOR, CONTRIBUTOR, CLIENT, GUEST],
    },
    {
        path: '/signup',
        name: 'signup',
        component: Signup,
        allowed: [ADMINISTRATOR, MODERATOR, CONTRIBUTOR, CLIENT, GUEST],
    },
    {
        path: '/home',
        name: 'home',
        component: Home,
        allowed: [ADMINISTRATOR, MODERATOR, CONTRIBUTOR, CLIENT, GUEST],
    },
    {
        path: '/dashboard',
        name: 'dashboard',
        component: Dashboard,
        allowed: [ADMINISTRATOR],
    },
    {
        path: '/users',
        name: 'users',
        component: Users,
        allowed: [ADMINISTRATOR],
    },
    {
        path: '/roles',
        name: 'roles',
        component: Roles,
        allowed: [ADMINISTRATOR],
    },
    {
        path: '/contributions',
        name: 'contributions',
        component: Contributions,
        allowed: [ADMINISTRATOR, MODERATOR, CONTRIBUTOR],
    },
    {
        path: '/contexts',
        name: 'contexts',
        component: Contexts,
        allowed: [ADMINISTRATOR, MODERATOR, CONTRIBUTOR],
    },
    {
        path: '/models',
        name: 'models',
        component: Models,
        allowed: [ADMINISTRATOR],
    },
    {
        path: '/not-found',
        name: 'notFound',
        component: NotFound,
        allowed: [ADMINISTRATOR, MODERATOR, CONTRIBUTOR, CLIENT, GUEST],
    },
    {
        path: '/not-authorized',
        name: 'notAuthorized',
        component: NotAuthorized,
        allowed: [ADMINISTRATOR, MODERATOR, CONTRIBUTOR, CLIENT, GUEST],
    },
]

const router = new VueRouter({
    mode: 'history',
    base: process.env.BASE_URL,
    routes,
})


router.beforeEach(async (to, from, next) => {
    if (['home', 'login', 'signup'].includes(to.name)) {
        return next()
    }
    const user = store.getters['authentication/user']
    const route = routes.find(route => route.name === to.name)
    if (!route.allowed.includes(user.role.label)) {
        return await router.push({ name: 'notAuthorized' })
    }
    if (!routes.map(route => route.path).includes(to.path)) {
        return await router.push({ name: 'notFound' })
    }
    if (!['home', 'login', 'signup'].includes(to.name)) {
        if (!store.getters['authentication/user']) {
            return await router.push({ name: 'home' })
        }
    }
    next()
})

export default router
