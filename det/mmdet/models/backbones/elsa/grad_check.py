"""
This file is modified from DDFNet: https://github.com/thefoxofsky/ddfnet
"""
import torch
from torch.autograd import gradcheck
from ipdb import set_trace

from .elsa import elsa_op


def py_forward(feat, channel_mul, channel_add, spatial_att, kernel_size, dilation, stride):
    assert stride == 1
    B, C, H, W = feat.shape
    out_python = torch.zeros(B, C, H, W, requires_grad=True, device='cuda:0').double()
    for b in range(B):
        for c in range(C):
            for y in range(H):
                for x in range(W):
                    for iy in range(kernel_size):
                        for ix in range(kernel_size):
                            if y+(iy-kernel_size//2)*dilation < 0 or y+(iy-kernel_size//2)*dilation >= H or x+(ix-kernel_size//2)*dilation < 0 or x+(ix-kernel_size//2)*dilation >= W:
                                continue
                            _combined_kernel = channel_mul[b, c, iy, ix] * spatial_att[
                                b, iy * kernel_size + ix, y, x] + channel_add[b, c, iy, ix]
                            out_python[b, c, y, x] += _combined_kernel * feat[b, c, y+(iy-kernel_size//2)*dilation, x+(ix-kernel_size//2)*dilation]
    return out_python


feat = torch.randn(1, 10, 15, 15, requires_grad=True, device='cuda:0').double()
channel_mul = torch.randn(1, 10, 3, 3, requires_grad=True, device='cuda:0').double()
channel_add = torch.randn(1, 10, 3, 3, requires_grad=True, device='cuda:0').double()
spatial_att = torch.randn(1, 9, 15, 15, requires_grad=True, device='cuda:0').double()

torch.cuda.empty_cache()

out_py = py_forward(feat, channel_mul, channel_add, spatial_att, 3, 1, 1)
out_elsa_o = elsa_op(feat, channel_mul, channel_add, spatial_att, 3, 1, 1, 'o')
out_elsa_f = elsa_op(feat, channel_mul, channel_add, spatial_att, 3, 1, 1, 'f')


if(float(((out_py-out_elsa_o) > 1e-5).sum()) == 0):
    print(True)
else:
    set_trace()
    exit(1)

if(float(((out_py-out_elsa_f) > 1e-5).sum()) == 0):
    print(True)
else:
    set_trace()
    exit(1)

torch.cuda.empty_cache()

feat = torch.randn(96, 64, 56, 56, requires_grad=True, device='cuda:0').double()
channel_mul = torch.randn(96, 64, 3, 3, requires_grad=True, device='cuda:0').double()
channel_add = torch.randn(96, 64, 3, 3, requires_grad=True, device='cuda:0').double()
spatial_att = torch.randn(96, 9, 56, 56, requires_grad=True, device='cuda:0').double()

out_elsa_o = elsa_op(feat, channel_mul, channel_add, spatial_att, 3, 1, 1, 'o')
out_elsa_f = elsa_op(feat, channel_mul, channel_add, spatial_att, 3, 1, 1, 'f')

if(float(((out_elsa_o-out_elsa_f) > 1e-10).sum()) == 0):
    print(True)
else:
    set_trace()
    exit(1)

torch.cuda.empty_cache()

feat = torch.randn(96, 128, 28, 28, requires_grad=True, device='cuda:0').double()
channel_mul = torch.randn(96, 128, 3, 3, requires_grad=True, device='cuda:0').double()
channel_add = torch.randn(96, 128, 3, 3, requires_grad=True, device='cuda:0').double()
spatial_att = torch.randn(96, 9, 28, 28, requires_grad=True, device='cuda:0').double()

out_elsa_o = elsa_op(feat, channel_mul, channel_add, spatial_att, 3, 1, 1, 'o')
out_elsa_f = elsa_op(feat, channel_mul, channel_add, spatial_att, 3, 1, 1, 'f')

if(float(((out_elsa_o-out_elsa_f) > 1e-10).sum()) == 0):
    print(True)
else:
    set_trace()
    exit(1)

torch.cuda.empty_cache()

feat = torch.randn(96, 256, 14, 14, requires_grad=True, device='cuda:0').double()
channel_mul = torch.randn(96, 256, 3, 3, requires_grad=True, device='cuda:0').double()
channel_add = torch.randn(96, 256, 3, 3, requires_grad=True, device='cuda:0').double()
spatial_att = torch.randn(96, 9, 14, 14, requires_grad=True, device='cuda:0').double()

out_elsa_o = elsa_op(feat, channel_mul, channel_add, spatial_att, 3, 1, 1, 'o')
out_elsa_f = elsa_op(feat, channel_mul, channel_add, spatial_att, 3, 1, 1, 'f')

if(float(((out_elsa_o-out_elsa_f) > 1e-10).sum()) == 0):
    print(True)
else:
    set_trace()
    exit(1)

torch.cuda.empty_cache()

feat = torch.randn(96, 512, 7, 7, requires_grad=True, device='cuda:0').double()
channel_mul = torch.randn(96, 512, 3, 3, requires_grad=True, device='cuda:0').double()
channel_add = torch.randn(96, 512, 3, 3, requires_grad=True, device='cuda:0').double()
spatial_att = torch.randn(96, 9, 7, 7, requires_grad=True, device='cuda:0').double()

out_elsa_o = elsa_op(feat, channel_mul, channel_add, spatial_att, 3, 1, 1, 'o')
out_elsa_f = elsa_op(feat, channel_mul, channel_add, spatial_att, 3, 1, 1, 'f')

if(float(((out_elsa_o-out_elsa_f) > 1e-10).sum()) == 0):
    print(True)
else:
    set_trace()
    exit(1)

torch.cuda.empty_cache()

print('All forward pass')

feat = torch.randn(1, 70, 10, 10, requires_grad=True, device='cuda:0').double()
channel_mul = torch.randn(1, 70, 3, 3, requires_grad=True, device='cuda:0').double()
channel_add = torch.randn(1, 70, 3, 3, requires_grad=True, device='cuda:0').double()
spatial_att = torch.randn(1, 9, 10, 10, requires_grad=True, device='cuda:0').double()

# check backwoard
test = gradcheck(elsa_op, (feat, channel_mul, channel_add, spatial_att, 3, 1, 1), atol=1e-5, eps=1e-3)
print(test)
test = gradcheck(elsa_op, (feat, channel_mul, channel_add, spatial_att, 3, 2, 1), atol=1e-5, eps=1e-3)
print(test)

spatial_att = torch.randn(1, 9, 5, 5, requires_grad=True, device='cuda:0').double()
torch.cuda.empty_cache()

test = gradcheck(elsa_op, (feat, channel_mul, channel_add, spatial_att, 3, 1, 2), atol=1e-5, eps=1e-3)
print(test)
test = gradcheck(elsa_op, (feat, channel_mul, channel_add, spatial_att, 3, 2, 2), atol=1e-5, eps=1e-3)
print(test)


feat = torch.randn(35, 1, 10, 10, requires_grad=True, device='cuda:0').double()
channel_mul = torch.randn(35, 1, 3, 3, requires_grad=True, device='cuda:0').double()
channel_add = torch.randn(35, 1, 3, 3, requires_grad=True, device='cuda:0').double()
spatial_att = torch.randn(35, 9, 10, 10, requires_grad=True, device='cuda:0').double()
torch.cuda.empty_cache()

# check backwoard
test = gradcheck(elsa_op, (feat, channel_mul, channel_add, spatial_att, 3, 1, 1), atol=1e-5, eps=1e-3)
print(test)
test = gradcheck(elsa_op, (feat, channel_mul, channel_add, spatial_att, 3, 2, 1), atol=1e-5, eps=1e-3)
print(test)

spatial_att = torch.randn(35, 9, 5, 5, requires_grad=True, device='cuda:0').double()
torch.cuda.empty_cache()

test = gradcheck(elsa_op, (feat, channel_mul, channel_add, spatial_att, 3, 1, 2), atol=1e-5, eps=1e-3)
print(test)
test = gradcheck(elsa_op, (feat, channel_mul, channel_add, spatial_att, 3, 2, 2), atol=1e-5, eps=1e-3)
print(test)

feat = torch.randn(1, 1, 50, 50, requires_grad=True, device='cuda:0').double()
channel_mul = torch.randn(1, 1, 3, 3, requires_grad=True, device='cuda:0').double()
channel_add = torch.randn(1, 1, 3, 3, requires_grad=True, device='cuda:0').double()
spatial_att = torch.randn(1, 9, 50, 50, requires_grad=True, device='cuda:0').double()
torch.cuda.empty_cache()

# check backwoard
test = gradcheck(elsa_op, (feat, channel_mul, channel_add, spatial_att, 3, 1, 1), atol=1e-5, eps=1e-3)
print(test)
test = gradcheck(elsa_op, (feat, channel_mul, channel_add, spatial_att, 3, 2, 1), atol=1e-5, eps=1e-3)
print(test)

spatial_att = torch.randn(1, 9, 25, 25, requires_grad=True, device='cuda:0').double()
torch.cuda.empty_cache()

test = gradcheck(elsa_op, (feat, channel_mul, channel_add, spatial_att, 3, 1, 2), atol=1e-5, eps=1e-3)
print(test)
test = gradcheck(elsa_op, (feat, channel_mul, channel_add, spatial_att, 3, 2, 2), atol=1e-5, eps=1e-3)
print(test)

feat = torch.randn(1, 70, 10, 10, requires_grad=True, device='cuda:0').double()
channel_mul = torch.randn(1, 70, 5, 5, requires_grad=True, device='cuda:0').double()
channel_add = torch.randn(1, 70, 5, 5, requires_grad=True, device='cuda:0').double()
spatial_att = torch.randn(1, 25, 10, 10, requires_grad=True, device='cuda:0').double()

# check backwoard
test = gradcheck(elsa_op, (feat, channel_mul, channel_add, spatial_att, 5, 1, 1), atol=1e-5, eps=1e-3)
print(test)
test = gradcheck(elsa_op, (feat, channel_mul, channel_add, spatial_att, 5, 2, 1), atol=1e-5, eps=1e-3)
print(test)

spatial_att = torch.randn(1, 25, 5, 5, requires_grad=True, device='cuda:0').double()
torch.cuda.empty_cache()

test = gradcheck(elsa_op, (feat, channel_mul, channel_add, spatial_att, 5, 1, 2), atol=1e-5, eps=1e-3)
print(test)
test = gradcheck(elsa_op, (feat, channel_mul, channel_add, spatial_att, 5, 2, 2), atol=1e-5, eps=1e-3)
print(test)


feat = torch.randn(20, 1, 10, 10, requires_grad=True, device='cuda:0').double()
channel_mul = torch.randn(20, 1, 5, 5, requires_grad=True, device='cuda:0').double()
channel_add = torch.randn(20, 1, 5, 5, requires_grad=True, device='cuda:0').double()
spatial_att = torch.randn(20, 25, 10, 10, requires_grad=True, device='cuda:0').double()
torch.cuda.empty_cache()

# check backwoard
test = gradcheck(elsa_op, (feat, channel_mul, channel_add, spatial_att, 5, 1, 1), atol=1e-5, eps=1e-3)
print(test)
test = gradcheck(elsa_op, (feat, channel_mul, channel_add, spatial_att, 5, 2, 1), atol=1e-5, eps=1e-3)
print(test)

spatial_att = torch.randn(20, 25, 5, 5, requires_grad=True, device='cuda:0').double()
torch.cuda.empty_cache()

test = gradcheck(elsa_op, (feat, channel_mul, channel_add, spatial_att, 5, 1, 2), atol=1e-5, eps=1e-3)
print(test)
test = gradcheck(elsa_op, (feat, channel_mul, channel_add, spatial_att, 5, 2, 2), atol=1e-5, eps=1e-3)
print(test)

feat = torch.randn(1, 1, 40, 40, requires_grad=True, device='cuda:0').double()
channel_mul = torch.randn(1, 1, 5, 5, requires_grad=True, device='cuda:0').double()
channel_add = torch.randn(1, 1, 5, 5, requires_grad=True, device='cuda:0').double()
spatial_att = torch.randn(1, 25, 40, 40, requires_grad=True, device='cuda:0').double()
torch.cuda.empty_cache()

# check backwoard
test = gradcheck(elsa_op, (feat, channel_mul, channel_add, spatial_att, 5, 1, 1), atol=1e-5, eps=1e-3)
print(test)
test = gradcheck(elsa_op, (feat, channel_mul, channel_add, spatial_att, 5, 2, 1), atol=1e-5, eps=1e-3)
print(test)

spatial_att = torch.randn(1, 25, 20, 20, requires_grad=True, device='cuda:0').double()
torch.cuda.empty_cache()

test = gradcheck(elsa_op, (feat, channel_mul, channel_add, spatial_att, 5, 1, 2), atol=1e-5, eps=1e-3)
print(test)
test = gradcheck(elsa_op, (feat, channel_mul, channel_add, spatial_att, 5, 2, 2), atol=1e-5, eps=1e-3)
print(test)

print('All backward pass')
exit(1)