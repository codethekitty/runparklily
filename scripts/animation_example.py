from pylab import *
import imageio

#%%
frame_path='frames/{i}.png'

x=linspace(0,2*pi,20)
y=sin(x)
for i in range(len(x)-1):
    figure()
    xlim(0,10)
    ylim(-1,1)
    plot(x[:i+1],y[:i+1],'o-')
    savefig(frame_path.format(i=i))
    
#%% syntax for making gif
images = []
for i in range(54):
    images.append(imageio.imread(frame_path.format(i=i)))
imageio.mimsave('top10.gif', images,duration=1)

#%% syntax for making mp4
writer = imageio.get_writer('test.mp4', fps=1)
frame_path='frames/{i}.png'

for i in range(54):
    writer.append_data(imageio.imread(frame_path.format(i=i)))
writer.close()


