// 所有镜头的数据配置
export type Shot = {
  id: number;
  startTime: number; // 秒
  duration: number; // 秒
  image: string;
  overlayVideo?: string;
  overlayOpacity?: number;
  blendMode?: 'normal' | 'multiply' | 'screen' | 'overlay' | 'darken' | 'lighten';
  transition?: 'fade' | 'flash' | 'dissolve' | 'lightLeak' | 'hardCut';
  text?: string;
  narration?: string;
  cameraMove?: 'static' | 'pushIn' | 'pullOut' | 'pan' | 'tilt' | 'shake';
  effect?: 'kenBurns' | 'glitch' | 'colorShift' | 'blur' | 'zoom';
};

export const fps = 30;
export const durationInSeconds = 160; // 2分40秒
export const durationInFrames = fps * durationInSeconds;

// 场景1：脆弱的网络世界（0:00 - 0:25）
export const scene1Shots: Shot[] = [
  {
    id: 1,
    startTime: 0,
    duration: 5,
    image: 'assets/images/global_network_earth.jpg',
    overlayVideo: 'assets/videos/earth_globe_rotating_space_4k.mp4',
    overlayOpacity: 0.4,
    blendMode: 'overlay',
    transition: 'fade',
    narration: '互联网。',
    cameraMove: 'pushIn',
    effect: 'kenBurns'
  },
  {
    id: 2,
    startTime: 5,
    duration: 5,
    image: 'assets/images/global_network_earth.jpg',
    overlayVideo: 'assets/videos/glitch_distortion_effect_4k.mp4',
    overlayOpacity: 0.5,
    blendMode: 'overlay',
    transition: 'flash',
    narration: '连接着数十亿人的生活。',
    cameraMove: 'shake',
    effect: 'glitch'
  },
  {
    id: 3,
    startTime: 10,
    duration: 5,
    image: 'assets/images/website_error_concept.jpg',
    overlayVideo: 'assets/videos/digital_noise_static_4k.mp4',
    overlayOpacity: 0.3,
    blendMode: 'overlay',
    transition: 'hardCut',
    text: 'ERROR 503\nCONNECTION FAILED',
    narration: '但你有没有想过——',
    cameraMove: 'static',
    effect: 'glitch'
  },
  {
    id: 4,
    startTime: 15,
    duration: 5,
    image: 'assets/images/stressed_user_computer.jpg',
    transition: 'dissolve',
    narration: '它比你想象的更脆弱。',
    cameraMove: 'static',
    effect: 'colorShift'
  },
  {
    id: 5,
    startTime: 20,
    duration: 5,
    image: '', // 黑屏
    transition: 'fade',
    cameraMove: 'static'
  }
];

// 场景2：改变，从质疑开始（0:25 - 0:55）
export const scene2Shots: Shot[] = [
  {
    id: 6,
    startTime: 25,
    duration: 5,
    image: 'assets/images/startup_office_team.jpg',
    overlayVideo: 'assets/videos/tech_particles_floating_hd.mp4',
    overlayOpacity: 0.25,
    blendMode: 'screen',
    transition: 'dissolve',
    narration: '2009年，两个不甘平庸的人站了出来。',
    cameraMove: 'pan',
    effect: 'kenBurns'
  },
  {
    id: 7,
    startTime: 30,
    duration: 5,
    image: 'assets/images/startup_office_team.jpg',
    overlayVideo: 'assets/videos/hud_interface_futuristic_4k.mp4',
    overlayOpacity: 0.2,
    blendMode: 'overlay',
    transition: 'hardCut',
    text: 'Cloudflare',
    narration: '他们问了一个问题——',
    cameraMove: 'pushIn',
    effect: 'kenBurns'
  },
  {
    id: 8,
    startTime: 35,
    duration: 5,
    image: 'assets/images/data_center_blue_lights.jpg',
    overlayVideo: 'assets/videos/data_flow_network_4k.mp4',
    overlayOpacity: 0.35,
    blendMode: 'overlay',
    transition: 'flash',
    narration: '为什么安全必须昂贵？',
    cameraMove: 'pushIn',
    effect: 'kenBurns'
  },
  {
    id: 9,
    startTime: 40,
    duration: 5,
    image: 'assets/images/data_center_blue_lights.jpg',
    overlayVideo: 'assets/videos/matrix_code_rain_4k.mp4',
    overlayOpacity: 0.15,
    blendMode: 'screen',
    transition: 'lightLeak',
    narration: '为什么性能要让步于预算？',
    cameraMove: 'tilt',
    effect: 'kenBurns'
  },
  {
    id: 10,
    startTime: 45,
    duration: 5,
    image: 'assets/images/global_network_map.jpg',
    overlayVideo: 'assets/videos/global_network_connections_4k.mp4',
    overlayOpacity: 0.4,
    blendMode: 'overlay',
    transition: 'hardCut',
    narration: 'Cloudflare，诞生于对现状的不妥协。',
    cameraMove: 'pullOut',
    effect: 'kenBurns'
  },
  {
    id: 11,
    startTime: 50,
    duration: 5,
    image: 'assets/images/global_network_map.jpg',
    overlayVideo: 'assets/videos/network_nodes_particles_4k.mp4',
    overlayOpacity: 0.45,
    blendMode: 'overlay',
    transition: 'dissolve',
    narration: '他们要做一件事——让每一个网站，都能拥有顶尖的安全和速度。不分大小，不问出身。',
    cameraMove: 'static',
    effect: 'kenBurns'
  }
];

// 场景3：无形的守护者（0:55 - 1:45）
export const scene3Shots: Shot[] = [
  {
    id: 12,
    startTime: 55,
    duration: 5,
    image: 'assets/images/engineers_monitoring_screens.jpg',
    overlayVideo: 'assets/videos/tech_data_background_4k.mp4',
    overlayOpacity: 0.25,
    blendMode: 'overlay',
    transition: 'hardCut',
    text: '300+ 数据中心',
    narration: '今天，Cloudflare 的网络遍布全球。',
    cameraMove: 'pan',
    effect: 'kenBurns'
  },
  {
    id: 13,
    startTime: 60,
    duration: 5,
    image: 'assets/images/engineers_monitoring_screens.jpg',
    overlayVideo: 'assets/videos/hud_interface_futuristic_4k.mp4',
    overlayOpacity: 0.3,
    blendMode: 'overlay',
    transition: 'flash',
    narration: '300 多个城市，连接着世界每一个角落。',
    cameraMove: 'pushIn',
    effect: 'kenBurns'
  },
  {
    id: 14,
    startTime: 65,
    duration: 5,
    image: 'assets/images/cybersecurity_shield.jpg',
    overlayVideo: 'assets/videos/energy_shield_force_field_4k.mp4',
    overlayOpacity: 0.5,
    blendMode: 'overlay',
    transition: 'hardCut',
    text: '3万亿次请求/天',
    narration: '每天，我们处理超过 3 万亿次请求。',
    cameraMove: 'static',
    effect: 'kenBurns'
  },
  {
    id: 15,
    startTime: 70,
    duration: 5,
    image: 'assets/images/cybersecurity_shield.jpg',
    overlayVideo: 'assets/videos/cybersecurity_tech_protection_hd.mp4',
    overlayOpacity: 0.4,
    blendMode: 'overlay',
    transition: 'dissolve',
    text: '拦截数十亿次攻击',
    narration: '拦截数十亿次攻击。',
    cameraMove: 'static',
    effect: 'kenBurns'
  },
  {
    id: 16,
    startTime: 75,
    duration: 10,
    image: 'assets/images/mother_online_shopping.jpg', // 主素材，会快速切换
    overlayVideo: 'assets/videos/geometric_network_lines_4k.mp4',
    overlayOpacity: 0.15,
    blendMode: 'overlay',
    transition: 'flash',
    narration: '当你在深夜网购时，当孩子在课堂上看视频时，当创业者实现梦想时——Cloudflare 都在背后，为你护航。',
    cameraMove: 'static',
    effect: 'kenBurns'
  },
  {
    id: 17,
    startTime: 85,
    duration: 5,
    image: 'assets/images/mother_online_shopping.jpg',
    overlayVideo: 'assets/videos/tech_particles_floating_hd.mp4',
    overlayOpacity: 0.2,
    blendMode: 'overlay',
    transition: 'lightLeak',
    narration: '它就像互联网的免疫系统——',
    cameraMove: 'static',
    effect: 'kenBurns'
  },
  {
    id: 18,
    startTime: 90,
    duration: 5,
    image: 'assets/images/student_online_learning.jpg',
    overlayVideo: 'assets/videos/data_flow_network_4k.mp4',
    overlayOpacity: 0.2,
    blendMode: 'overlay',
    transition: 'lightLeak',
    narration: '默默无闻，却无处不在。',
    cameraMove: 'static',
    effect: 'kenBurns'
  },
  {
    id: 19,
    startTime: 95,
    duration: 10,
    image: 'assets/images/small_business_owner.jpg',
    overlayVideo: 'assets/videos/network_nodes_particles_4k.mp4',
    overlayOpacity: 0.25,
    blendMode: 'overlay',
    transition: 'fade',
    cameraMove: 'static',
    effect: 'kenBurns'
  }
];

// 场景4：更公平的互联网（1:45 - 2:15）
export const scene4Shots: Shot[] = [
  {
    id: 20,
    startTime: 105,
    duration: 10,
    image: 'assets/images/enterprise_server_room.jpg', // 左侧
    overlayVideo: 'assets/videos/data_flow_network_4k.mp4',
    overlayOpacity: 0.3,
    blendMode: 'overlay',
    transition: 'dissolve',
    narration: '有人问，Cloudflare 是什么？我们说——它是让互联网变得更公平的力量。',
    cameraMove: 'static',
    effect: 'kenBurns'
  },
  {
    id: 21,
    startTime: 115,
    duration: 10,
    image: 'assets/images/diverse_team_computers.jpg',
    overlayVideo: 'assets/videos/geometric_network_lines_4k.mp4',
    overlayOpacity: 0.2,
    blendMode: 'overlay',
    transition: 'flash',
    text: 'Equality. Security. Speed.',
    narration: '让小企业也能拥有大企业的安全防护。让个人博客也能享受世界级的加速技术。让每一个人的声音，都能被世界听见。',
    cameraMove: 'pan',
    effect: 'kenBurns'
  },
  {
    id: 22,
    startTime: 125,
    duration: 10,
    image: 'assets/images/diverse_team_computers.jpg',
    overlayVideo: 'assets/videos/hud_interface_futuristic_4k.mp4',
    overlayOpacity: 0.25,
    blendMode: 'overlay',
    transition: 'dissolve',
    narration: '这不是技术炫耀。这是我们的信仰。',
    cameraMove: 'pullOut',
    effect: 'kenBurns'
  }
];

// 场景5：未来已来（2:15 - 2:40）
export const scene5Shots: Shot[] = [
  {
    id: 23,
    startTime: 135,
    duration: 5,
    image: 'assets/images/smart_city_robots.jpg',
    overlayVideo: 'assets/videos/tech_data_background_4k.mp4',
    overlayOpacity: 0.3,
    blendMode: 'overlay',
    transition: 'flash',
    narration: '互联网的未来，正在被重新定义。',
    cameraMove: 'pushIn',
    effect: 'kenBurns'
  },
  {
    id: 24,
    startTime: 140,
    duration: 10,
    image: 'assets/images/smart_home_iot.jpg', // 快速切换三个素材
    overlayVideo: 'assets/videos/network_nodes_particles_4k.mp4',
    overlayOpacity: 0.25,
    blendMode: 'overlay',
    transition: 'flash',
    text: '边缘计算 | AI | 无服务器',
    narration: '边缘计算、人工智能、无服务器架构——Cloudflare 站在最前沿。',
    cameraMove: 'static',
    effect: 'kenBurns'
  },
  {
    id: 25,
    startTime: 150,
    duration: 10,
    image: 'assets/images/earth_from_space.jpg',
    overlayVideo: 'assets/videos/earth_zoom_from_space_4k.mp4',
    overlayOpacity: 0.35,
    blendMode: 'overlay',
    transition: 'fade',
    text: 'Cloudflare - 帮助构建更好的互联网\nHelping Build a Better Internet',
    narration: '我们守护的不只是网站。是每一个连接。是每一份信任。是整个互联网的明天。',
    cameraMove: 'pullOut',
    effect: 'kenBurns'
  }
];

export const allShots = [
  ...scene1Shots,
  ...scene2Shots,
  ...scene3Shots,
  ...scene4Shots,
  ...scene5Shots
];
