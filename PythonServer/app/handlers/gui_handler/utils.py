# -*- coding: utf-8 -*-

# python imports
import math

# chillin imports
from chillin_server.gui.reference_manager import default_reference_manager as drm
from chillin_server.gui.scene_actions import \
    (InstantiateBundleAsset, ChangeTransform, EndCycle, ChangeRenderer, ChangeCamera,
     ChangeLight, CreateBasicObject, ChangeIsActive, ChangeText, ChangeSlider, ChangeAudioSource,
     Asset, Vector3, Vector4, EBasicObjectType, ECameraClearFlag, ELightShadowType, EDefaultParent)


def create_asset(world, asset_name, parent_ref=None, parent_child_ref=None, cycle=None, is_ui=False):
    ref = drm.new()
    world.scene.add_action(InstantiateBundleAsset(
        ref = ref,
        cycle = cycle,
        parent_ref = parent_ref,
        parent_child_ref = parent_child_ref,
        asset = Asset(bundle_name='main', asset_name=asset_name),
        default_parent = EDefaultParent.RootObject if not is_ui else EDefaultParent.RootCanvas,
    ))

    return ref


def change_transform(world, ref, child_ref=None, cycle=None, duration_cycles=None,
                     position=None, y_rotation=None, z_scale=None, change_local=True):
    world.scene.add_action(ChangeTransform(
        ref = ref,
        child_ref = child_ref,
        cycle = cycle,
        duration_cycles = duration_cycles,
        position = position,
        rotation = None if y_rotation is None else Vector3(y=y_rotation),
        scale = None if z_scale is None else Vector3(z=z_scale),
        change_local = change_local,
    ))


def change_scale(world, ref, x_scale=None, y_scale=None, z_scale=None):
    world.scene.add_action(ChangeTransform(
        ref = ref,
        scale = Vector3(x=x_scale, y=y_scale, z=z_scale),
        change_local = True,
    ))


def change_material(world, ref, asset_name):
    world.scene.add_action(ChangeRenderer(
        ref = ref,
        material_asset = Asset(bundle_name='main', asset_name=asset_name),
    ))


def create_main_light(world):
    main_light = drm.new()
    world.scene.add_action(CreateBasicObject(
        ref = main_light,
        type = EBasicObjectType.Light,
    ))
    world.scene.add_action(ChangeTransform(
        ref = main_light,
        rotation = Vector3(x = 90, y = 90, z = 0),
    ))
    world.scene.add_action(ChangeLight(
        ref = main_light,
        intensity = 1,
        indirect_multiplier = 0,
        color = Vector4(x=1, y=1, z=1, w=1),
        shadow_type = ELightShadowType.Disabled,
    ))


def init_main_camera(world):
    max_x = -world.GUI_X_OFFSET + 3
    max_z = -world.GUI_Z_OFFSET + 12

    aspect_ratio = 3/2
    fov = 90
    max_y_x = max_x / aspect_ratio / math.tan(math.radians(fov / 2))  # max_y based on max_x
    max_y_z = max_z / math.tan(math.radians(fov / 2))  # max_y based on max_z

    max_y = max(max_y_x, max_y_z)

    world.scene.add_action(ChangeCamera(
        ref = drm.get('MainCamera'),
        is_orthographic = False,
        clear_flag = ECameraClearFlag.SolidColor,
        background_color = Vector4(x = 0/255, y = 0/255, z = 30/255, w = 1),
        min_position = Vector3(x = -max_x, y = 1, z = -max_z),
        max_position = Vector3(x = max_x, y = max_y, z = max_z),
        field_of_view = 90,
        max_zoom = 120,
        min_zoom = 20,
    ))
    world.scene.add_action(ChangeTransform(
        ref = drm.get('MainCamera'),
        position = Vector3(x=0, y=max_y, z=2),
        rotation = Vector3(x=90, y=0, z=0),
    ))


def change_is_active(world, ref, is_active, child_ref=None, cycle=None):
    world.scene.add_action(ChangeIsActive(
        ref = ref,
        child_ref = child_ref,
        cycle = cycle,
        is_active = is_active,
    ))


def change_text(world, ref, child_ref=None, text=None):
    world.scene.add_action(ChangeText(
        ref = ref,
        child_ref = child_ref,
        text = text,
    ))


def change_slider(world, ref, child_ref, value, duration_cycles):
    world.scene.add_action(ChangeSlider(
        ref = ref,
        child_ref = child_ref,
        duration_cycles = duration_cycles,
        value = value,
    ))


def change_audio(world, ref, child_ref=None, clip=None, play=True, time=0, cycle=None, loop=None, volume=None):
    asset = Asset(bundle_name='main', asset_name=clip) if clip != None else None

    world.scene.add_action(ChangeAudioSource(
        ref = ref,
        child_ref = child_ref,
        cycle = cycle,
        audio_clip_asset = asset,
        play = play,
        time = time,
        loop = loop,
        volume = volume,
    ))


def end_cycle(world):
    world.scene.add_action(EndCycle())
