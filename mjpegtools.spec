Name:           mjpegtools
Version:        1.9.0
Release:        0.6.rc3%{?dist}
Summary:        Tools to manipulate MPEG data

Group:          Applications/Multimedia
License:        GPLv2
URL:            http://mjpeg.sourceforge.net/
Source0:        http://downloads.sourceforge.net/mjpeg/%{name}-%{version}rc3.tar.gz
Patch0:         %{name}-1.9.0rc1-anytovcd-ffmpegver.patch
Patch1:         http://sources.gentoo.org/viewcvs.py/*checkout*/gentoo-x86/media-video/mjpegtools/files/mjpegtools-1.9.0_rc3-gcc43.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  libjpeg-devel
BuildRequires:  nasm
BuildRequires:  libdv-devel
BuildRequires:  SDL-devel >= 1.1.3
BuildRequires:  SDL_gfx-devel
BuildRequires:  libquicktime-devel >= 0.9.8
BuildRequires:  libpng-devel
BuildRequires:  gtk2-devel >= 2.4.0
Requires:       %{name}-libs = %{version}-%{release}
# mencoder for lav2avi.sh
Requires:       mencoder
# ffmpeg main package, y4mscaler and which for anytovcd.sh
Requires:       ffmpeg
Requires:       y4mscaler
Requires:       which
Requires(post): /sbin/install-info
Requires(preun): /sbin/install-info

%description
The mjpeg programs are a set of tools that can do recording of videos
and playback, simple cut-and-paste editing and the MPEG compression of
audio and video under Linux.  This package contains mjpegtools console
utilities.

%package        gui
Summary:        GUI tools to manipulate MPEG data
Group:          Applications/Multimedia
Requires:       %{name} = %{version}-%{release}

%description    gui
The mjpeg programs are a set of tools that can do recording of videos
and playback, simple cut-and-paste editing and the MPEG compression of
audio and video under Linux.  This package contains mjpegtools GUI
utilities.

%package        libs
Summary:        Libraries used by mjpegtools
Group:          System Environment/Libraries
Requires:       libquicktime >= 0.9.8

%description    libs
The mjpeg programs are a set of tools that can do recording of videos
and playback, simple cut-and-paste editing and the MPEG compression of
audio and video under Linux.  This package contains libraries used by
mjpegtools.

%package        devel
Summary:        Development files for mjpegtools libraries 
Group:          Development/Libraries
Requires:       %{name}-libs = %{version}-%{release}
Requires:       pkgconfig

%description    devel
The mjpeg programs are a set of tools that can do recording of videos
and playback, simple cut-and-paste editing and the MPEG compression of
audio and video under Linux.  This package contains development files
for building applications that use mjpegtools libraries.


%prep 
%setup -q -n %{name}-%{version}rc3
find . -type d -name CVS -print0 | xargs -0 rm -rf
%patch0 -p1
%patch1 -p1
sed -i -e 's/ARCHFLAGS=.*/ARCHFLAGS=/' configure*
sed -i -e 's|/lib /usr/lib|/%{_lib} %{_libdir}|' configure # lib64 rpaths
for f in docs/yuvfps.1 ; do
    iconv -f iso-8859-1 -t utf-8 $f > $f.utf8 ; mv $f.utf8 $f
done


%build
%configure --disable-dependency-tracking --disable-static
make # %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
rm -f $RPM_BUILD_ROOT{%{_infodir}/dir,%{_libdir}/lib*.la}
# too broken/outdated to be useful in 1.[89].0 (and would come with dep chain)
rm -f $RPM_BUILD_ROOT%{_bindir}/mpegtranscode


%clean
rm -rf $RPM_BUILD_ROOT


%post libs -p /sbin/ldconfig

%postun libs -p /sbin/ldconfig

%post
/sbin/install-info %{_infodir}/mjpeg-howto.info %{_infodir}/dir || :

%preun
[ $1 -eq 0 ] && \
/sbin/install-info --delete %{_infodir}/mjpeg-howto.info %{_infodir}/dir || :


%files
%defattr(-,root,root,-)
%doc COPYING CHANGES ChangeLog AUTHORS BUGS README.lavpipe NEWS TODO
%{_bindir}/*
%exclude %{_bindir}/glav
%exclude %{_bindir}/lavplay
%exclude %{_bindir}/y4mhist
%exclude %{_bindir}/yuvplay
%{_mandir}/man1/*.1*
%exclude %{_mandir}/man1/lavplay.1*
%exclude %{_mandir}/man1/yuvplay.1*
%{_mandir}/man5/yuv4mpeg.5*
%{_infodir}/mjpeg-howto.info*

%files gui
%defattr(-,root,root,-)
%doc README.glav
%{_bindir}/glav
# lavplay and yuvplay won't save -libs/console util users from X11 and SDL
# dependencies as long as liblavplay is in -libs, but they're inherently
# GUI tools -> include them here
%{_bindir}/lavplay
%{_bindir}/y4mhist
%{_bindir}/yuvplay
%{_mandir}/man1/lavplay.1*
%{_mandir}/man1/yuvplay.1*

%files libs
%defattr(-,root,root,-)
%doc COPYING
%{_libdir}/lib*.so.*

%files devel
%defattr(-,root,root,-)
%{_includedir}/%{name}
%{_libdir}/lib*.so
%{_libdir}/pkgconfig/%{name}.pc


%changelog
* Fri Jul 25 2008 Hans de Goede <j.w.r.degoede@hhs.nl> 1.9.0-0.6.rc3
- Release bump for rpmfusion
- Sync with freshrpms (no changes)

* Tue Apr 22 2008 Ville Skyttä <ville.skytta at iki.fi> - 1.9.0-0.5.rc3
- Apply patch from Gentoo to fix build with GCC 4.3 (#1941).

* Tue Dec  4 2007 Ville Skyttä <ville.skytta at iki.fi> - 1.9.0-0.4.rc3
- 1.9.0rc3.

* Sat Sep 29 2007 Ville Skyttä <ville.skytta at iki.fi> - 1.9.0-0.4.rc2
- Requires: which

* Wed Aug 22 2007 Ville Skyttä <ville.skytta at iki.fi> - 1.9.0-0.3.rc2
- License: GPLv2

* Thu Jun 21 2007 Ville Skyttä <ville.skytta at iki.fi> - 1.9.0-0.2.rc2
- Rebuild.

* Fri Jun  8 2007 Ville Skyttä <ville.skytta at iki.fi> - 1.9.0-0.1.rc2
- 1.9.0rc2.

* Sat Nov 25 2006 Ville Skyttä <ville.skytta at iki.fi> - 1.8.0-7
- Split GUI utilities into -gui subpackage.
- Don't ship mpegtranscode, it's broken/outdated.
- Require mencoder for lav2avi.sh.

* Fri Oct 06 2006 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> 1.8.0-6
- rebuilt for unwind info generation, broken in gcc-4.1.1-21

* Sun Sep 24 2006 Ville Skyttä <ville.skytta at iki.fi> - 1.8.0-5
- Specfile cleanup.

* Sun Jun  4 2006 Ville Skyttä <ville.skytta at iki.fi> - 1.8.0-4
- Get rid of undefined non-weak symbols in liblav*.
- Apply upstream fix for compiling with libquicktime 0.9.8.

* Thu Mar 09 2006 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- switch to new release field

* Tue Feb 28 2006 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- add dist

* Sat Jan 21 2006 Ville Skyttä <ville.skytta at iki.fi> - 1.8.0-0.lvn.3
- Include license text in -libs, it can be installed without the main package.
- Convert yuvfps man page to UTF-8.
- Fix -devel Group tag.

* Thu Jan 19 2006 Adrian Reber <adrian@lisas.de> - 1.8.0-0.lvn.2
- Added patch to compile with gcc 4.1
- Dropped 0 Epoch

* Mon Sep 19 2005 Ville Skyttä <ville.skytta at iki.fi> - 0:1.8.0-0.lvn.1
- 1.8.0.

* Sat Aug 27 2005 Ville Skyttä <ville.skytta at iki.fi> - 0:1.6.3-0.lvn.0.1.rc3
- 1.6.3-rc3, Altivec fixes applied upstream.

* Fri Aug 12 2005 Ville Skyttä <ville.skytta at iki.fi> - 0:1.6.3-0.lvn.0.1.rc2
- 1.6.3-rc2, clean up obsolete pre-FC2 stuff.
- Fix Altivec build, kudos to upstream.

* Thu May 26 2005 Ville Skyttä <ville.skytta at iki.fi> - 0:1.6,3-0.lvn.0.1.rc1
- 1.6.3-rc1 (1.7.0 snapshot package not released, so no Epoch bump).

* Sun May 22 2005 Ville Skyttä <ville.skytta at iki.fi> - 0:1.7.0-0.lvn.0.2.cvs20050521
- PPC: disable Altivec due to gcc4 build failure, honor $RPM_OPT_FLAGS.

* Sat May 21 2005 Ville Skyttä <ville.skytta at iki.fi> - 0:1.7.0-0.lvn.0.1.cvs20050521
- Pre-1.7.0 snapshot as of today, all patches applied or obsoleted upstream.
- Require pkgconfig in -devel.

* Wed Feb  2 2005 Ville Skyttä <ville.skytta at iki.fi> - 0:1.6.2-0.lvn.7
- Add corrected -fPIC tweak from Thorsten.

* Mon Jan 31 2005 Ville Skyttä <ville.skytta at iki.fi> - 0:1.6.2-0.lvn.6
- Include PNG input support.
- Remove no-op $RPM_OPT_FLAGS setting from %%build.
- Remove bogus optimization settings from configure script.

* Fri Dec 31 2004 Thorsten Leemhuis <fedora[AT]leemhuis[DOT]info> - 0:1.6.2-0.lvn.5
- CFLAGS="$CFLAGS -fPIC" on non x86; Fixes build error on x86_64; The 
  option --with-pic is not enough

* Sat Dec 18 2004 Dams <anvil[AT]livna.org> - 0:1.6.2-0.lvn.4
- Disabling static libraries building

* Tue Dec 14 2004 Ville Skyttä <ville.skytta at iki.fi> - 0:1.6.2-0.lvn.3
- Include quicktime support.
- Apply patch from ALT Linux to fix info pages, fix typo in %%post.
- Require /sbin/install-info.
- Add "--without static" rpmbuild option to work around an issue with FC3 strip
- Always enable SIMD accelerations, CPU capabilities detected at runtime.
- Always disable use of cmov.

* Thu Nov 11 2004 Dams <anvil[AT]livna.org> 0:1.6.2-0.lvn.2
- Added patch to fix gcc3.4 build
- Detected race condition in Makefiles (disabling _smp_mflags use)
- Added info files & scriptlets
- Dropped patch0 and patch1

* Tue Jun  8 2004 Dams <anvil[AT]livna.org> 0:1.6.2-0.lvn.1
- Updated to 1.6.2

* Sun Sep 28 2003 Dams <anvil[AT]livna.org> 0:1.6.1-0.fdr.6
- Removed comment after scriptlets

* Fri Aug 22 2003 Dams <anvil[AT]livna.org> 0:1.6.1-0.fdr.5
- buildroot -> RPM_BUILD_ROOT

* Sun Aug 10 2003 Dams <anvil[AT]livna.org> 0:1.6.1-0.fdr.4
- Applied upstream patches to fix build on gcc3.3 systems

* Tue Apr 29 2003 Dams <anvil[AT]livna.org> 0:1.6.1-0.fdr.3
- Now test arch for configure options (from Ville)
- Removed ImageMagick-devel BuildRequires

* Sun Apr 27 2003 Dams <anvil[AT]livna.org> 0:1.6.1-0.fdr.2
- Added missing BuildRequires 
- Added post/postun scriplets for libs package

* Wed Apr 23 2003 Dams <anvil[AT]livna.org> 
- Initial build.
