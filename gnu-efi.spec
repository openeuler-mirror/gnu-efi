%define debug_package %{nil}
Name:          gnu-efi
Version:       3.0.8
Release:       11
Summary:       Development Libraries and headers for EFI
Epoch:         1
License:       BSD
URL:           ftp://ftp.hpl.hp.com/pub/linux-ia64
ExclusiveArch: x86_64 aarch64
Source0:       https://sourceforge.net/projects/gnu-efi/files/gnu-efi-3.0.8.tar.bz2
#stubs-32.h comes from http://www.gnu.org/software/glibc/
Source1:       stubs-32.h
Patch0:        fix-clang.patch

%global efidir %(eval echo $(grep ^ID= /etc/os-release | sed  's/^ID=//'))

%ifarch x86_64
%global efiarch x86_64
%endif
%ifarch aarch64
%global efiarch aarch64
%endif

Provides:  %{name}-utils = %{epoch}:%{version}-%{release}
Obsoletes: %{name}-utils < %{epoch}:%{version}-%{release}
BuildRequires:	gcc

%description
This package contains development headers and libraries for developing
applications that run under EFI (Extensible Firmware Interface).

%package devel
Summary:   Development Libraries and headers for EFI
Obsoletes: gnu-efi < 1:3.0.2-1
Requires:  gnu-efi

%description devel
This package contains development headers and libraries for developing
applications that run under EFI (Extensible Firmware Interface).

%prep
%autosetup  -n gnu-efi-3.0.8 -p1
install -d gnuefi/gnu
install -Dp %{SOURCE1} gnuefi/gnu/

%build
%if "%toolchain" == "clang"
	export LDFLAGS='-z,relro -z,now'
%endif
make
make apps
%ifarch x86_64
setarch linux32 -B make ARCH=ia32 PREFIX=%{_prefix} LIBDIR=%{_prefix}/lib
setarch linux32 -B make ARCH=ia32 PREFIX=%{_prefix} LIBDIR=%{_prefix}/lib apps
%endif

%install
install -d %{buildroot}/%{_libdir}/gnuefi
install -d %{buildroot}/boot/efi/EFI/%{efidir}/%{efiarch}
make PREFIX=%{_prefix} LIBDIR=%{_libdir} INSTALLROOT=%{buildroot} install
mv %{buildroot}/%{_libdir}/*.lds %{buildroot}/%{_libdir}/*.o %{buildroot}/%{_libdir}/gnuefi
mv %{efiarch}/apps/{route80h.efi,modelist.efi} %{buildroot}/boot/efi/EFI/%{efidir}/%{efiarch}/

%ifarch x86_64
install -d %{buildroot}/%{_prefix}/lib/gnuefi
install -d %{buildroot}/boot/efi/EFI/%{efidir}/ia32

setarch linux32 -B make PREFIX=%{_prefix} LIBDIR=%{_prefix}/lib INSTALLROOT=%{buildroot} ARCH=ia32 install
mv %{buildroot}/%{_prefix}/lib/*.{lds,o} %{buildroot}/%{_prefix}/lib/gnuefi/
mv ia32/apps/{route80h.efi,modelist.efi} %{buildroot}/boot/efi/EFI/%{efidir}/ia32/
%endif

%files
%{_prefix}/lib*/*
%dir %attr(0700,root,root) /boot/efi/EFI/%{efidir}/*/
%attr(0700,root,root) /boot/efi/EFI/%{efidir}/*/*.efi

%files devel
%defattr(-,root,root,-)
%doc README.* ChangeLog
%{_includedir}/efi

%changelog
* Tue May 16 2023 yoo <sunyuechi@iscas.ac.cn> - 3.0.8-11
- fix clang build error

* Mon Jun 7 2021 baizhonggui <baizhonggui@huawei.com> - 3.0.8-10
- Fix building error: make[1]: gcc: No such file or directory
- Add gcc in BuildRequires

* Thu Sep 10 2020 liuweibo <liuweibo10@huawei.com> - 3.0.8-9
- Fix Source0

* Wed Mar 18 2020 likexin <likexin4@huawei.com> - 3.0.8-8
- Delete modify-cflags.patch

* Wed Mar 18 2020 likexin <likexin4@huawei.com> - 3.0.8-7
- Fix up modify-cflags.patch

* Wed Mar 18 2020 likexin <likexin4@huawei.com> - 3.0.8-6
- Add cflags -fstack-protector-strong

* Fri Mar 13 2020 zhujunhao<zhujunhao5@huawei.com> - 3.0.8-5
- Modify x86 build failed

* Wed Jan 15 2020 yuxiangyang4<yuxiangyang4@huawei.com> - 3.0.8-4
- Upgrade source code to 3.0.8

* Wed Nov 20 2019 yangjian<yangjian79@huawei.com> - 3.0.8-3
- Package init
