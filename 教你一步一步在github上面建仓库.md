## 教你一步一步在github上面建仓库
这是我自己第一次在github上面建仓库的心得总结。

用了好久的github，但都是下载别人的源代码，自己从来没有建过仓库。实际上也就没有完整使用过git工具。

为了准备开发我的Python IDE项目，这个是肯定要建开源项目的。因为之前没有完整用过git，所以我决定自己建一个测试用的仓库。

动手前找了下学习资料，首先是《猴子都能懂的git入门》，但它介绍的是小海龟，我想用命令行工具，所以pass掉它。

接着找到了《万字详解！Git入门最佳实践》、《一个小时两万字学会Git》和《我看谁还不懂Git》，但看来看去他们都有一个共同特点：理论介绍详细，但命令都是散的，跟一本命令手册一样，并不会一步步教你怎么新建一个仓库。甚至连到哪里去下载git客户端工具也没说。

算了，懒得找了，自己一步步琢磨着来吧。折腾了一晚上，终于建好了第一个仓库。

**首先，准备好梯子，这一步没有的话，下面就不用看了。**
### 一、服务器准备
接下来先是在github上的操作（官网是https://github.com/）：

1. 注册github账号
2. 登录github，点击右上角的“+”号，选择“New repository” **（特别注意，不要选择project。我第一次就搞错了，结果后面才发现）** 
3. 输入仓库名称(我的是DownloadTs)，描述，选择公开(或私有)，确定
4. 点击刚才新建的仓库，点击“Clone or download”按钮，复制仓库地址

到这里，服务器上的事情就完成了，接下来是客户端的操作。

### 二、下载客户端
首先是到github上下载客户端，下载地址是：
https://git-scm.com/download/
如果嫌慢，也可以用国内的：
https://git-scm.cn/downloads
可以选择安装版和解压版，安装版里面有GUI工具，不过我选择的是解压版。

解压之后有两个工具，一个叫git-bash,一个叫git-cmd。我用的是git-cmd，因为它的操作跟windows的命令行差不多。而git-bash是linux风格的，用起来不习惯。

### 三、使用git客户端
在使用git-cmd之前，还要做点准备工作，首先是要在本机建立一个工作区，与服务器上的仓库相对应，以后编程都可以在这里进行：

打开资源管理器，找到你自己的编程目录，然后新建一个子目录，名字可以和你在服务器上建的仓库名称相同。

然后在命令行（cmd）里切换到这个目录，接下来就是用git-cmd在本机上的操作了：

**1. 进入git**

在命令行输入以下命令：
```
D:\Program\PythonProgram\DownloadTs>git-cmd 
```
*注意：如果用的解压版，这个git-cmd命令并不在默认的系统搜索路径下，所以要先找到它的安装目录，比如d:\git,在系统环境中添加这条路径。或者用d:\git\git-cmd来启动它。*

启动git-cmd之后，你几乎感觉不到它的存在，看上去还像是在cmd控制台，但你只要输入“git"，就会出现一系列的信息，表示已经在git-cmd命令行里面了。

**2. 克隆仓库**

首先，你需要知道服务器上的仓库地址，复制到你的本地电脑上（前面已经说过了）。接着输入以下命令：
```
git clone 复制的仓库地址 
```
等待下载完成，然后在本地电脑上打开刚才下载的仓库文件夹，可以看到里面有个README.md文件，说明仓库已经成功创建。
在仓库文件夹里，输入以下命令：
```
git status
```
这时会看到当前仓库的状态，当前应该是空的。

**3. 建立空仓库**

不过，你也可以自己新建一个空仓库，然后再跟服务器上的仓库联系起来，我就是用的这种方法。
输入下面的命令：
```
git init
```
这时会出现一系列信息，并在最后显示
```
Initialized empty Git repository in D:/Program/PythonProgram/DownloadTs/.git/
```
这样的提示，表示仓库已经成功创建。

这时用资源管理器可以看到在仓库文件夹下生成了一个.git文件夹。不过这个文件夹在命令行下面是隐藏的，需要用“dir /a”才能显示

**4. 配置用户信息**

接下来要配置一下你的用户名和邮箱，输入以下命令：
```
git config user.name 你的用户名
git config user.email 你的邮箱
```
配置成功之后，可以在配置文件中看到相关信息。这个配置文件在.git下面，文件名叫config。

**5. 配置仓库**

现在这个空仓库还没有和服务器上的仓库对应起来（如果不是克隆下来的话），需要修改config这个配置文件。这个文件没有扩展名，可以用普通的记事本打开，然后在最后面加上这样一个小节的信息：
```
[remote "origin"]
	url = https://账号名:密码@github.com/newstarse/DownloadTs.git
	fetch = +refs/heads/*:refs/remotes/origin/*
    pushurl = https://github.com/newstarse/DownloadTs.git
```
这个小节的意思是，告诉git，服务器上的仓库地址是什么，账号和密码是什么，以及从服务器上拉取代码的规则。
配置完并保存之后，可以用下面的命令看一下是否成功：
```
git remote -v
```
如果成功，就会返回服务器的仓库地址和名字。

**6. 添加文件**

接下来可以把要上传的代码文件复制到仓库的主目录下面，如果需要修改的话，按照正常的代码编写规则修改保存即可。
当代码完成之后，就可以开始准备提交到服务器上了。
首先要输入以下命令暂存：
```
git add [file1] [file2] ...
```
这时会把你要提交的文件暂存起来，等待提交。实际上，它只是在.git文件夹下面生成一个暂存区，并不会真正影响代码。

接下来，把暂存区的文件提交到仓库区：
```
git commit [file1] [file2] ... -m [message]
```
如果后面没有m参数的话，会打开一个编辑器，输入提交信息，保存并退出。
注意：这个时候，代码其实还在本地，并没有真正提交到服务器上去。

**7. 提交代码**

一切就绪之后，就可以提交代码了，提交代码的命令如下：
```
git push
```
这里不需要带其它参数，因为远程服务器地址、用户名和密码我都已经在config文件里面配置好了。

但是，第一次做一定会失败，它会返回信息：
```
fatal: The current branch master has no upstream branch.
To push the current branch and set the remote as upstream, use

    git push --set-upstream origin master
```
也就是说，你还没有设置远程仓库的跟踪分支，所以你需要先设置一下。

输入以下命令：
```
git push --set-upstream origin master
```
但是这个命令也有很大的概率会失败，返回的信息是：
```
fatal: unable to access 'https://github.com/newstarse/DownloadTs.git/': Recv failure: Connection was reset
```
表示无法连接到远程服务器，虽然我可以用浏览器访问这个网址，但是git工具却访问不到，因为git用了不同的代理。

第一种方法是删除git工具自己的代理设置：
```
git config --global --unset https.proxy
git  config --global --unset http.proxy
```
再测试一下，可能会返回：
```
fatal: unable to access 'https://github.com/newstarse/DownloadTs.git/': Failed to connect to github.com port 443 after 21132 ms: Could not connect to server
```
这是因为不用代理的话，国内连接github非常不稳定。

所以更好的方法，是将git的代理设置成你梯子的代理。一般的梯子会设置系统代理，使用它这个设置才能成功。
打开计算机的系统设置，搜索“代理服务器设置”，打开后找到“手动设置代理”，点击“设置”，就可以看到你梯子当前设置的代理端口，比如我的是2800。这时候，可以在git里面使用这个设置了，命令如下：
```
git config --global http.proxy http://127.0.0.1:2800
git config --global https.proxy http://127.0.0.1:2800
```
*注意：这个端口号不同的梯子不一样*

设置完成后，再次执行push命令，这时候会弹出窗口提示，要求输入用户名和密码，在浏览器里面做无感认证，按照提示输入就行。*（我没太明白，明明在配置文件中已经保存了这些信息，为啥还要再输入一次？）*

到这时候，就会返回成功的信息了。然后可以到github上面看到你刚刚上传的代码文件了。

以上是最简单的过程，还未涉及到分支、合并、查找版本差异等功能，在以后的日子里，我会慢慢加上这些东西。


