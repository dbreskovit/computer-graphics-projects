from OpenGL.GL import *
from OpenGL.GL import shaders

VERTEX_SHADER = """
#version 120
varying vec2 vTexCoord;
varying vec3 vNormal;
varying vec3 vViewPosition;

void main() {
    vTexCoord = gl_MultiTexCoord0.st;
    vNormal = normalize(gl_NormalMatrix * gl_Normal);
    vec4 viewPos = gl_ModelViewMatrix * gl_Vertex;
    vViewPosition = -viewPos.xyz;
    gl_Position = gl_ModelViewProjectionMatrix * gl_Vertex;
}
"""

FRAGMENT_SHADER = """
#version 120
uniform sampler2D tex;
uniform float uTime;

varying vec2 vTexCoord;
varying vec3 vNormal;
varying vec3 vViewPosition;

void main() {
    float time = uTime * 0.05;
    vec2 offset1 = vec2(time, sin(vTexCoord.x * 10.0 + time) * 0.01);
    
    vec2 offset2 = vec2(-time * 0.8, cos(vTexCoord.y * 5.0 + time) * 0.01);

    vec4 color1 = texture2D(tex, vTexCoord + offset1);
    vec4 color2 = texture2D(tex, vTexCoord + offset2);

    vec3 baseColor = mix(color1.rgb, color2.rgb, 0.5); 

    vec3 normal = normalize(vNormal);
    vec3 viewDir = normalize(vViewPosition);
    float rim = 1.0 - max(dot(viewDir, normal), 0.0);

    rim = pow(rim, 4.5); 

    vec3 atmosphere = vec3(1.0, 0.4, 0.0) * rim * 1.5;

    gl_FragColor = vec4(baseColor + atmosphere, 1.0);
}
"""

def compile_sun_shader():
    try:
        shader = shaders.compileProgram(
            shaders.compileShader(VERTEX_SHADER, GL_VERTEX_SHADER),
            shaders.compileShader(FRAGMENT_SHADER, GL_FRAGMENT_SHADER)
        )
        return shader
    except Exception as e:
        print(f"Erro ao compilar Shader: {e}")
        return None