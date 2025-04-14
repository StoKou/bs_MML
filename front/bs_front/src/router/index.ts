import { createRouter, createWebHistory } from 'vue-router'

import HomePage from '@/views/HomePage.vue'
import SearchPage from '@/views/SearchPage.vue'
import ShowPage from '@/views/ShowPage.vue'
import LayoutPage from '@/views/layout/LayoutPage.vue'
import LoginPage from '@/views/login/LoginPage.vue'
import UserProfile from '@/views/user2/UserProfile.vue'
import UserAvatar from '@/views/user2/UserAvatar.vue'
import UserPassword from '@/views/user2/UserPassword.vue'
import { useUserStore } from '@/stores'

const routes = [
  {
    path: '/login',
    component: LoginPage,
  },
  {
    path: '/',
    component: LayoutPage,
    redirect: '/home',
    children: [
      {
        path: '/home',
        component: HomePage,
      },
      { path: '/search', component: SearchPage },
      { path: '/show', component: ShowPage },
      {
        path: '/user/profile',
        component: UserProfile,
      },
      {
        path: '/user/avatar',
        component: UserAvatar,
      },
      {
        path: '/user/password',
        component: UserPassword,
      },
    ],
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

router.beforeEach((to) => {
  // 如果没有token, 且访问的是非登录页，拦截到登录，其他情况正常放行
  const useStore = useUserStore()
  if (!useStore.token && to.path !== '/login') return '/login'
})
export default router
